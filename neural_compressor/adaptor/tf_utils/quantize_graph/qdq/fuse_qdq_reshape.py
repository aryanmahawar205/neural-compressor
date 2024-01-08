#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Quantize the Reshape."""

import tensorflow as tf
from tensorflow.python.framework import dtypes
from tensorflow.core.framework import node_def_pb2, attr_value_pb2

from neural_compressor.adaptor.tf_utils.quantize_graph_common import QuantizeGraphHelper as helper
from neural_compressor.adaptor.tf_utils.util import version1_eq_version2, version1_gt_version2, version1_lt_version2

from ..quantize_graph_base import QuantizeNodeBase


class FuseNodeStartWithReshape(QuantizeNodeBase):
    """Quantize the Reshape."""

    def __init__(self, **kwargs):
        """Initialization."""
        super().__init__(**kwargs)
        self.exclude_nodes = []
        self.sorted_patterns = sorted(self.patterns, key=lambda i: len(i), reverse=True)

    def _add_reshape_function(self, original_node, quantized_op_node, quantize_input_node):
        """Set quantized reshape node attributes."""
        if quantize_input_node.op == "Dequantize":
            quantized_op_node.attr["T"].CopyFrom(attr_value_pb2.AttrValue(type=quantize_input_node.attr["T"].type))
            helper.copy_attr(quantized_op_node, "Tshape", original_node.attr["Tshape"])
            return
            
        helper.copy_attr(quantized_op_node , "T", original_node.attr["T"])
        helper.copy_attr(quantized_op_node , "Tshape", original_node.attr["Tshape"])
        

    def _apply_reshape_quantization(self, match_node_name):
        """Quantize Reshape.

        Dequantize + Reshape + QuantizeV2
        """
        apply_quant = False
        skip_node_name = match_node_name[2:]
        matched_node = self.node_name_mapping[match_node_name[1]].node
        control_inputs, normal_inputs = self._get_node_input(matched_node.name)
        dequantize_node = self.node_name_mapping[normal_inputs[0]].node
        quantize_node = self.node_name_mapping[dequantize_node.input[0]].node
        quantize_input_node =  self.node_name_mapping[quantize_node.input[0]].node

        # only apply quantization when the previous node is a int8 node
        # expect dq + q + dq + reshape
        if quantize_input_node.op == "Dequantize":
            apply_quant = True
            quantize_node.attr["T"].CopyFrom(attr_value_pb2.AttrValue(type=quantize_input_node.attr["T"].type))
            all_input_names = [dequantize_node.input[0], normal_inputs[1]] + dequantize_node.input[1:]
        else:
            self.exclude_nodes.append(matched_node.name)
            skip_node_name.append(quantize_node.name)
            all_input_names = [quantize_input_node.name, normal_inputs[1]]

        skip_node_name.append(normal_inputs[0])

        for _, node in enumerate(self.input_graph.node):
            if node.name in skip_node_name:
                self.logger.debug("skip node {}".format(node.name))
            elif node.name == match_node_name[1]:
                if not apply_quant:
                    quantized_reshape_node = helper.create_node("Reshape", node.name, all_input_names)
                    self._add_reshape_function(node, quantized_reshape_node, quantize_input_node)
                    self.add_output_graph_node(quantized_reshape_node)
                    continue

                self.logger.debug("Matched node {} with input {}.".format(node.name, node.input))
                quantized_op_name = node.name + "_eightbit_quantized"
                quantized_op_type = "QuantizedReshape"

                quantized_reshape_node = helper.create_node(quantized_op_type, quantized_op_name, all_input_names)

                self._add_reshape_function(node, quantized_reshape_node, quantize_input_node)
                self.add_output_graph_node(quantized_reshape_node)

                deq_type = dtypes.DType(quantize_input_node.attr["T"].type)
                self._intel_cpu_add_dequantize_result_node(
                    quantized_op_name, node.name, dtype=deq_type, performance_only=self.performance_only
                )
            else:
                new_node = node_def_pb2.NodeDef()
                new_node.CopyFrom(node)
                self.add_output_graph_node(new_node)

    def get_longest_fuse(self):
        """Get the longest fusion pattern."""
        self._get_op_list()
        matched_node_name = []

        for k, v in enumerate(self.op_list):
            if v in set(fusion[1] for fusion in self.sorted_patterns):
                cur_node = self.node_name_mapping[list(self.node_name_mapping.keys())[k]].node

                if cur_node.name != self.start_node_name:
                    continue

                for sub_rule in self.sorted_patterns:
                    if sub_rule[0] != "Dequantize" or sub_rule[-1] != "QuantizeV2":
                        continue
                    if v != sub_rule[1]:
                        continue
                    matched_node_name.clear()
                    matched_node_name.append(sub_rule[0])
                    matched_node_name.append(cur_node.name)
                    matched_node_name.append(sub_rule[-1])
                    return sub_rule, matched_node_name
        return None, None

    def apply_the_transform(self):
        """Quantize Reshape."""
        self._get_op_list()
        matched_rule, matched_node_name = self.get_longest_fuse()
        if matched_node_name:
            fusion_name = "".join(matched_rule)
            if fusion_name == "DequantizeReshapeQuantizeV2":
                self._apply_reshape_quantization(matched_node_name)
            else:  # pragma: no cover
                self.logger.info("Unknown fusion pattern {}.".format(fusion_name))
                if self.remove_redundant_quant_flag:
                    self.input_graph = self.remove_redundant_quantization(self.input_graph)
                return self.input_graph, self.exclude_nodes

            self.input_graph = self.output_graph
            self._reset_output_node_maps()
            if self.remove_redundant_quant_flag:
                self.output_graph = self.remove_redundant_quantization(self.output_graph)
            return self.output_graph, self.exclude_nodes

        if self.remove_redundant_quant_flag:
            self.input_graph = self.remove_redundant_quantization(self.input_graph)
        return self.input_graph, self.exclude_nodes
