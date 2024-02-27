# Copyright (c) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import json
import os
import re
import subprocess
import torch
import cpuinfo
import numpy
import psutil
import intel_extension_for_pytorch as ipex
from collections import UserDict
from packaging.version import Version

from neural_compressor.torch.utils import (
    get_ipex_version, 
    get_torch_version, 
    logger, 
    simple_inference,
    unify_op_type_mapping_ipex,
    TransformerBasedModelBlockPatternDetector,
    ipex_config_path,
    paser_cfgs,
    get_quantizable_ops_from_cfgs,
)

version = get_torch_version()
ipex_ver = get_ipex_version()


def generate_activation_observer(scheme, algorithm, smooth_quant=False, smooth_quant_enable=False):  # pragma: no cover
    """This is a helper method to generate an activation observer.

    Args:
        scheme (str): Quantization scheme to be used.
        algorithm (str): What algorithm for computing the quantization parameters based on.

    Returns:
        An observer.
    """
    kl_activation_observer = {
        "name": "HistogramObserver",
        "bins": 2048,
        "upsample_rate": 128,
        "dtype": "torch.quint8",
        "qscheme": "torch.per_tensor_affine",
        "reduce_range": False,
        "quant_min": 0,
        "quant_max": 255,
    }
    minmax_activation_observer = {
        "name": "MinMaxObserver",
        "dtype": "torch.quint8",
        "qscheme": "torch.per_tensor_affine",
        "reduce_range": False,
        "quant_min": 0,
        "quant_max": 255,
    }
    smoothquant_kl_activation_observer = {
        "name": "SmoothQuantActivationObserver",
        "smooth_quant_enabled": smooth_quant_enable,
        "dtype": "torch.quint8",
        "qscheme": "torch.per_tensor_affine",
        "reduce_range": False,
        "quant_min": 0,
        "quant_max": 255,
        "alpha": 0.5,
        "act_observer": kl_activation_observer,
        "act_ic_observer": {
            "name": "PerChannelMinMaxObserver",
            "ch_axis": -1,
            "dtype": "torch.quint8",
            "qscheme": "torch.per_channel_affine",
            "reduce_range": False,
            "quant_min": 0,
            "quant_max": 255,
        },
    }
    smoothquant_minmax_activation_observer = {
        "name": "SmoothQuantActivationObserver",
        "smooth_quant_enabled": smooth_quant_enable,
        "dtype": "torch.quint8",
        "qscheme": "torch.per_tensor_affine",
        "reduce_range": False,
        "quant_min": 0,
        "quant_max": 255,
        "alpha": 0.5,
        "act_observer": minmax_activation_observer,
        "act_ic_observer": {
            "name": "PerChannelMinMaxObserver",
            "ch_axis": -1,
            "dtype": "torch.quint8",
            "qscheme": "torch.per_channel_affine",
            "reduce_range": False,
            "quant_min": 0,
            "quant_max": 255,
        },
    }
    REDUCE_RANGE = False if CpuInfo().vnni else True
    if REDUCE_RANGE:
        minmax_activation_observer["reduce_range"] = REDUCE_RANGE
        kl_activation_observer["reduce_range"] = REDUCE_RANGE
    if scheme == "sym":
        minmax_activation_observer["qscheme"] = "torch.per_tensor_symmetric"
        minmax_activation_observer["dtype"] = "torch.qint8"
        minmax_activation_observer["quant_min"] = -128
        minmax_activation_observer["quant_max"] = 127
        kl_activation_observer["qscheme"] = "torch.per_tensor_symmetric"
        kl_activation_observer["dtype"] = "torch.qint8"
        kl_activation_observer["quant_min"] = -128
        kl_activation_observer["quant_max"] = 127
    if smooth_quant and smooth_quant_enable:
        if algorithm == "kl":
            return smoothquant_kl_activation_observer
        if algorithm == "minmax":
            return smoothquant_minmax_activation_observer
    else:
        if algorithm == "kl":
            return kl_activation_observer
        if algorithm == "minmax":
            return minmax_activation_observer


def check_cfg_and_qconfig(
    tune_cfg, cfgs, op_infos_from_cfgs, output_tensor_ids_op_name, smooth_quant=False
):  # pragma: no cover
    """Check configs and quantization configs.

    Args:
        tune_cfg (dict): dictionary of quantization configuration.
        cfgs (dict): the input configs.
        op_infos_from_cfgs (dict): op infos from configs.
        output_tensor_ids_op_name (dict): dictionary of output tensor op names.

    Returns:
        cfgs (dict).
    """
    for op_name in tune_cfg:
        inc_op_cfg = tune_cfg[op_name]
        for i, name in enumerate(op_name[0]):
            # to int8
            ipex_op_cfg = op_infos_from_cfgs[name]
            input_tensor_infos = ipex_op_cfg["input_tensor_infos"]
            if op_name[1] == "Linear" or op_name[1] == "Linear&add":  # record op_name for possible op-wise fallback
                logger.debug(f"ipex_op_cfg['fqn'] - op_name {ipex_op_cfg['fqn']}  {op_name}")
            for index, input_tensor_info in enumerate(input_tensor_infos):
                if "force_dtype" not in input_tensor_info.keys():
                    continue
                if (
                    input_tensor_info["force_dtype"] == "torch.qint8"
                    or input_tensor_info["force_dtype"] == "torch.quint8"
                ):
                    # int8 -> int8
                    if inc_op_cfg["weight"]["dtype"] == "int8":
                        inc_scheme = inc_op_cfg["activation"]["scheme"]
                        inc_algorithm = inc_op_cfg["activation"]["algorithm"]
                        ipex_op_cfg["input_tensor_infos"] = input_tensor_infos
                        if (
                            "op_type" in ipex_op_cfg
                            and ipex_op_cfg["op_type"] == "<class 'torch.nn.modules.linear.Linear'>"
                        ):
                            smooth_quant_enable = True
                        else:
                            smooth_quant_enable = False
                        activation_observer = generate_activation_observer(
                            inc_scheme, inc_algorithm, smooth_quant, smooth_quant_enable
                        )
                        if not smooth_quant:
                            if inc_scheme == "sym":
                                input_tensor_infos[index]["force_dtype"] = "torch.qint8"
                            if inc_scheme == "asym":
                                input_tensor_infos[index]["force_dtype"] = "torch.quint8"
                        ipex_op_cfg["activation_observer"] = activation_observer
                    # int8 -> fp32
                    else:
                        input_tensor_infos[index]["force_dtype"] = "torch.float32"
                    # modify pre_op output inf_dtype
                    if i == 0:
                        input_tensor_id = input_tensor_info["id"]
                        input_tensor_dtype = input_tensor_info["force_dtype"]
                        if input_tensor_id in output_tensor_ids_op_name.keys():
                            pre_op_name = output_tensor_ids_op_name[input_tensor_id]
                            pre_op_module = pre_op_name[0][0]
                            pre_op_state = pre_op_name[0][1]
                            pre_op_index = pre_op_name[0][2]
                            pre_op_infos = cfgs[pre_op_module][pre_op_state][pre_op_index]
                            pre_op_output_infos = pre_op_infos["output_tensor_infos"]
                            for index, pre_op_output in enumerate(pre_op_output_infos):
                                if pre_op_output["id"] == input_tensor_id:
                                    pre_op_output_infos[index]["inf_dtype"] = input_tensor_dtype
                                else:
                                    pass
                            pre_op_infos["output_tensor_infos"] = pre_op_output_infos
                            cfgs[pre_op_module][pre_op_state][pre_op_index] = pre_op_infos
                        else:
                            pass
            cfgs[name[0]][name[1]][name[2]] = ipex_op_cfg
    return cfgs


def cfg_to_qconfig(
    tune_cfg, cfgs, op_infos_from_cfgs, output_tensor_id_op_name, smooth_quant=False
):  # pragma: no cover
    assert cfgs is not None, "No configure for IPEX int8 model..."
    op_infos = copy.deepcopy(op_infos_from_cfgs)
    cfgs = check_cfg_and_qconfig(tune_cfg["op"], cfgs, op_infos, output_tensor_id_op_name, smooth_quant)
    with open(ipex_config_path, "w") as write_f:
        json.dump(cfgs, write_f, indent=4)
    return None


def get_quantizable_ops_recursively(model, example_inputs): # pragma: no cover
    """Get all quantizable ops from model.

    Args:
        model (object): input model
        example_inputs (dict|list|tuple|torch.Tensor): used to trace torch model.
    Returns:
        quantizable_ops (list): list of tuples of op_name and op_type.
        cfgs (dict): dict of configuration
    """
    quantizable_ops = []
    # group ops by position for transform-based model
    detector = TransformerBasedModelBlockPatternDetector(model)
    detect_result = detector.detect_block()
    attention_block = detect_result.get("attention_blocks", None)
    ffn_blocks = detect_result.get("ffn_blocks", None)
    logger.info(f"Attention Blocks: {len(attention_block)}")
    logger.info(f"FFN Blocks: {len(ffn_blocks)}")
    if not os.path.exists(ipex_config_path):
        assert isinstance(model, torch.nn.Module), "The model passed in is not the instance of torch.nn.Module"

    if hasattr(model, "save_qconf_summary"):  # pragma: no cover
        os.makedirs(os.path.dirname(ipex_config_path), exist_ok=True)
        model.save_qconf_summary(qconf_summary=ipex_config_path)
    else:
        model.eval()

        # create a quantization config file for intel pytorch extension model
        os.makedirs(os.path.dirname(ipex_config_path), exist_ok=True)
        assert example_inputs is not None, "IPEX need q_dataloader or example_inputs to prepare the model"
        from torch.ao.quantization import MinMaxObserver, PerChannelMinMaxObserver, QConfig

        if ipex_ver.release >= Version("2.1").release:
            # HistogramObserver will cause a performance issue.
            # static_qconfig = ipex.quantization.default_static_qconfig_mapping
            qconfig = QConfig(
                activation=MinMaxObserver.with_args(qscheme=torch.per_tensor_affine, dtype=torch.quint8),
                weight=PerChannelMinMaxObserver.with_args(dtype=torch.qint8, qscheme=torch.per_channel_symmetric),
            )
            from torch.ao.quantization import QConfigMapping

            static_qconfig = QConfigMapping().set_global(qconfig)
        else:
            static_qconfig = QConfig(
                activation=MinMaxObserver.with_args(qscheme=torch.per_tensor_affine, dtype=torch.quint8),
                weight=PerChannelMinMaxObserver.with_args(dtype=torch.qint8, qscheme=torch.per_channel_symmetric),
            )

        if isinstance(example_inputs, dict):
            model = ipex.quantization.prepare(model, static_qconfig, example_kwarg_inputs=example_inputs, inplace=True)
        else:
            model = ipex.quantization.prepare(model, static_qconfig, example_inputs=example_inputs, inplace=True)
        simple_inference(model, example_inputs, iterations=1)
        model.save_qconf_summary(qconf_summary=ipex_config_path)

    map_op_name_to_fqn = {}
    with open(ipex_config_path, "r") as f:
        cfgs = json.load(f)
        if ipex_ver.release < Version("1.12.0").release:  # pragma: no cover
            for op_cfg in cfgs:
                if op_cfg["name"] in unify_op_type_mapping_ipex:
                    quantizable_ops.append((op_cfg["id"], unify_op_type_mapping_ipex[op_cfg["name"]]))
                else:
                    re_flag = False
                    for pattern, unify_op_type in unify_op_type_mapping_ipex["re"].items():
                        if re.match(pattern, op_cfg["name"]):
                            re_flag = True
                            quantizable_ops.append((op_cfg["id"], unify_op_type))
                            break
                    if not re_flag:
                        quantizable_ops.append((op_cfg["id"], op_cfg["name"]))
        else:
            (
                ops_name,
                op_infos_from_cfgs,
                input_tensor_id_op_name,
                output_tensor_id_op_name,
            ) = paser_cfgs(cfgs)
            quantizable_op_names = get_quantizable_ops_from_cfgs(ops_name, op_infos_from_cfgs, input_tensor_id_op_name)
            for name in quantizable_op_names:
                # name : list
                if len(name) == 1:
                    module_key = name[0][0]
                    op_cfg_id = name[0][2]
                    ipex_op_type = cfgs[module_key]["q_op_infos"][op_cfg_id]["op_type"]
                    module_fqn = cfgs[module_key]["q_op_infos"][op_cfg_id].get("fqn", None)

                    if ipex_op_type in unify_op_type_mapping_ipex:
                        quantizable_ops.append((tuple(name), unify_op_type_mapping_ipex[ipex_op_type]))
                        map_op_name_to_fqn[(tuple(name), ipex_op_type)] = module_fqn
                    else:
                        re_flag = False
                        for pattern, unify_op_type in unify_op_type_mapping_ipex["re"].items():
                            if re.match(pattern, ipex_op_type):
                                re_flag = True
                                quantizable_ops.append((tuple(name), unify_op_type))
                                map_op_name_to_fqn[(tuple(name), unify_op_type)] = module_fqn
                                break
                        if not re_flag:
                            quantizable_ops.append((tuple(name), ipex_op_type))
                            map_op_name_to_fqn[(tuple(name), ipex_op_type)] = module_fqn
                else:
                    op_type = ""
                    for op_name in name:
                        module_key = op_name[0]
                        op_cfg_id = op_name[2]
                        single_op_type = cfgs[module_key]["q_op_infos"][op_cfg_id]["op_type"]
                        if single_op_type in unify_op_type_mapping_ipex:
                            single_op_type = unify_op_type_mapping_ipex[single_op_type]
                        op_type += "&" + single_op_type if op_type else single_op_type
                    quantizable_ops.append((tuple(name), op_type))
                    _module_key = name[0][0]
                    _op_cfg_id = name[0][2]
                    module_fqn = cfgs[_module_key]["q_op_infos"][_op_cfg_id]["fqn"]
                    map_op_name_to_fqn[(tuple(name), op_type)] = module_fqn

    logger.debug("Map op name to fqn: ")
    logger.debug(map_op_name_to_fqn)
    logger.info("Attention Blocks : ")
    logger.info(attention_block)
    logger.info("FFN Blocks : ")
    logger.info(ffn_blocks)
    return quantizable_ops, cfgs, op_infos_from_cfgs, output_tensor_id_op_name


def get_parent(node, all_parents=False): # pragma: no cover
    if node.inputs() is None:
        return None
    elif len(list(node.inputs())) == 0:
        return None
    if not all_parents:
        return list(node.inputs())[0].node()
    else:
        return list(node.inputs())


def get_module(model, key): # pragma: no cover
    """Get module from model by key name.

    Args:
        model (torch.nn.Module): original model
        key (str): module name to be replaced
    """
    module = model
    name_list = key.split(".")
    for name in name_list:
        if hasattr(module, name):
            module = getattr(module, name)
        elif hasattr(module, "sq_linear"):  # for peft models
            module = getattr(module, "sq_linear")
            module = getattr(module, name)
        elif hasattr(module, "orig_layer"):  # for peft models and auto alpha
            module = getattr(module, "orig_layer")
            module = getattr(module, name)
        else:
            module = module
    return module


def set_module(model, key, new_module): # pragma: no cover
    """Set new module into model by key name.

    Args:
        model (torch.nn.Module): original model
        key (str): module name to be replaced
        new_module (torch.nn.Module): new module to be inserted
    """
    module = model
    name_list = key.split(".")
    for name in name_list[:-1]:
        if hasattr(module, name):
            module = getattr(module, name)
        elif hasattr(module, ("sq_linear")):  # for peft models that Linears are contained in Linear
            module = getattr(module, "sq_linear")
            module = getattr(module, name)
        elif hasattr(module, ("orig_layer")):  # for peft models and auto alpha
            module = getattr(module, "orig_layer")
            module = getattr(module, name)
        else:
            module = module

    if hasattr(module, "sq_linear") and name_list[-1] != "sq_linear":  # for peft models
        module = getattr(module, "sq_linear")
    if hasattr(module, "orig_layer") and name_list[-1] != "orig_layer":  # for peft models and auto alpha
        module = getattr(module, "orig_layer")
    setattr(module, name_list[-1], new_module)


def update_sq_scale(ipex_config_path, smoothquant_scale_info): # pragma: no cover
    """Update ipex_config.json with smoothquant scale info generated by our algorithm.

    Args:
        ipex_config_path (str): a path to temporary ipex_config.json file.
        smoothquant_scale_info (dict): a dict contains smoothquant scale info.
    """
    with open(ipex_config_path, "r") as f:
        ipex_config = json.load(f)
        for module_name, v in ipex_config.items():
            if "q_op_infos" in v and v["q_op_infos"]:
                for op_num, v1 in v["q_op_infos"].items():
                    # update alpha data instead of updating weight scale
                    op_name = v1["fqn"]  # fqn always exists even it's empty.
                    if op_name in smoothquant_scale_info and v1["op_type_is_module"]:
                        input_scale_for_mul = smoothquant_scale_info[op_name]["input_scale_for_mul"].tolist()
                        input_scale_after_mul = smoothquant_scale_info[op_name]["input_scale_after_mul"].tolist()
                        input_zero_point_after_mul = smoothquant_scale_info[op_name][
                            "input_zero_point_after_mul"
                        ].tolist()
                        weight_scale_for_mul = (1 / smoothquant_scale_info[op_name]["input_scale_for_mul"]).tolist()
                        weight_scale_after_mul = smoothquant_scale_info[op_name]["weight_scale_after_mul"].tolist()
                        v1["input_tensor_infos"][0]["scale"] = input_scale_after_mul
                        v1["input_tensor_infos"][0]["zero_point"] = input_zero_point_after_mul
                        v1["input_tensor_infos"][0]["smooth_quant_scaling_factor"] = input_scale_for_mul
                        v1["weight_tensor_infos"][0]["smooth_quant_scaling_factor"] = weight_scale_for_mul
                        v1["weight_tensor_infos"][0]["scale"] = weight_scale_after_mul
                        # # observers were overridden by the fallback step, setting it back.
        f.close()
    # overwrite ipex_config_path
    with open(ipex_config_path, "w") as f1:
        json.dump(ipex_config, f1, indent=4)
        f1.close()


def enough_memo_store_scale(device, need_space): # pragma: no cover
    if device == "cuda":  # pragma: no cover
        current_gpu_index = torch.cuda.current_device()
        total_memory = torch.cuda.get_device_properties(current_gpu_index).total_memory
        used_memory = torch.cuda.memory_allocated(current_gpu_index)
        free_space = total_memory - used_memory
    else:
        import psutil

        free_space = psutil.virtual_memory().free
    return free_space >= need_space


def move_input_to_device(input, device=torch.device("cpu")): # pragma: no cover
    if isinstance(input, dict) or isinstance(input, UserDict):
        tmp_input = {}
        for k, inp in input.items():
            tmp_input[k] = move_input_to_device(inp, device)
        input = tmp_input
    elif isinstance(input, list) or isinstance(input, tuple):
        is_tuple = isinstance(input, tuple)
        tmp_input = []
        for inp in input:
            tmp_input.append(move_input_to_device(inp, device))
        input = tuple(tmp_input) if is_tuple else tmp_input
    elif isinstance(input, torch.Tensor):
        input = input.to(device)  # pylint: disable=no-member
    return input


def forward_wrapper(model, input, device=torch.device("cpu")): # pragma: no cover
    try:
        model = model.to(device)
        input = move_input_to_device(input, device)
    except Exception as e:
        logger.warning(e)
        logger.warning("Please check the input device if the error raised.")
    if isinstance(input, dict) or isinstance(input, UserDict):
        output = model(**input)
    elif isinstance(input, list) or isinstance(input, tuple):
        try:
            output = model(*input)
        except:
            output = model(input)
    else:
        output = model(input)
    return output


def model_forward(model, dataloader, iters, device): # pragma: no cover
    try:
        cnt = 0
        for idx, (input, label) in enumerate(dataloader):
            output = forward_wrapper(model, input, device)
            cnt += 1
            if iters != -1 and cnt >= iters:
                break
    except Exception as e:
        cnt = 0
        for idx, input in enumerate(dataloader):
            output = forward_wrapper(model, input, device)
            cnt += 1
            if iters != -1 and cnt >= iters:
                break


def cal_scale(input_max, weights, alpha, scale_type="orig"): # pragma: no cover
    if scale_type == "orig":  # same as the paper
        weights = torch.cat(weights, dim=0)
        weight_max = torch.max(torch.abs(weights), dim=0)[0]
        input_power = torch.pow(input_max, alpha)
        logger.debug(f"{max(input_max)}, {min(input_max)}")
        weight_power = torch.pow(weight_max, 1 - alpha)
        scale = torch.clip(input_power / weight_power, min=1e-5)
        scale[input_power == 0] = 1.0
        if input_power.size() == weight_power.size():
            scale[weight_power == 0] = 0.0  ##FIXME
        return scale


def model_forward_per_sample(model, sample, device): # pragma: no cover
    try:
        output = forward_wrapper(model, sample, device)
        return output

    except Exception as e:
        output = forward_wrapper(model, sample[0], device)
        return output


def quant_dequant_w(m, num_bits=8, scheme="sym"): # pragma: no cover
    eps = torch.finfo(torch.float32).eps
    if isinstance(m, torch.nn.Linear):
        x = m.weight
        tmp = torch.zeros(torch.max(x, dim=1).values.size())
        if scheme == "sym":
            q_min, q_max = -(2.0 ** (num_bits - 1)), 2.0 ** (num_bits - 1) - 1.0
            x_max = torch.max(torch.abs(x), dim=1).values
            scale = x_max / (float(q_max - q_min) / 2)
        else:
            q_min, q_max = 0, 2.0**num_bits - 1.0
            x_max = torch.maximum(torch.max(x, dim=1).values, tmp)
            x_min = torch.minimum(torch.min(x, dim=1).values, tmp)
            scale = (x_max - x_min) / (2**num_bits - 1)

        scale = torch.clip(scale, min=eps)

        if scheme == "sym":
            bias = 0
        else:
            bias = torch.round(0 - (torch.min(x, dim=1).values) / scale)
            bias = bias.unsqueeze(dim=-1)
        scale = scale.unsqueeze(dim=-1)
        q_x = torch.round(x / scale + bias)
        q_x.clamp_(q_min, q_max)
        return (q_x - bias) * scale
    elif isinstance(m, torch.nn.Conv2d):
        x = m.weight
        x = torch.permute(x, (0, 2, 3, 1))
        x = x.reshape(-1, x.shape[-1])
        tmp = torch.zeros(torch.max(x, dim=0).values.size())
        if scheme == "sym":
            q_min, q_max = -(2.0 ** (num_bits - 1)), 2.0 ** (num_bits - 1) - 1.0
            x_max = torch.max(torch.abs(x), dim=0).values
            scale = x_max / (2 ** (num_bits - 1) - 1)
        else:
            q_min, q_max = 0, 2.0**num_bits - 1.0
            x_max = torch.maximum(torch.max(x, dim=0).values, tmp)
            x_min = torch.minimum(torch.min(x, dim=0).values, tmp)
            scale = (x_max - x_min) / (2**num_bits - 1)
        scale = torch.clip(scale, min=eps)
        if scheme == "sym":
            bias = 0
        else:
            bias = torch.round(0 - (torch.min(x, dim=0).values) / scale)
            bias = bias.unsqueeze(dim=0)
        scale = scale.unsqueeze(dim=0)

        q_x = x / scale + bias
        q_x.clamp_(q_min, q_max).round_()
        q_dq_x = (q_x - bias) * scale
        q_dq_x = q_dq_x.view(m.weight.shape[0], m.weight.shape[2], m.weight.shape[3], m.weight.shape[1])
        q_dq_x = torch.permute(q_dq_x, (0, 3, 1, 2))
        return q_dq_x
    else:
        logger.warning("unsupported layer type, please have a check")


def quant_dequant_x(x, min_x=None, max_x=None, num_bits=8): # pragma: no cover
    eps = torch.finfo(torch.float32).eps
    q_min, q_max = 0, 2.0**num_bits - 1.0
    if max_x is None or min_x is None:
        max_x, min_x = torch.max(x), torch.min(x)
    else:
        max_x = torch.max(max_x)
        min_x = torch.min(min_x)
    scale = (max_x - min_x) / (2**num_bits - 1)
    scale = torch.clip(scale, min=eps)
    bias = torch.round((0 - min_x) / scale)
    q_x = torch.round(x / scale + bias)
    q_x.clamp_(q_min, q_max)
    return scale * (q_x - bias)


def reshape_scale_as_weight(layer, scale): # pragma: no cover
    """Reshape the scale for weight input channel, depthwise output channel
    :param layer:  torch module
    :param scale: orig scale
    :return: reshaped scale."""
    if hasattr(layer, "orig_layer"):
        layer = layer.orig_layer
    if isinstance(layer, torch.nn.Conv2d) and layer.groups > 1:  ##only depthwise conv could hit here
        scale = scale.view(scale.shape[0], 1, 1, 1)  ##mount on output channel

    elif isinstance(layer, torch.nn.Conv2d):
        scale = scale.view(1, scale.shape[0], 1, 1)

    elif isinstance(layer, torch.nn.Linear):
        scale = scale.view(1, scale.shape[0])

    return scale


def reshape_in_channel_to_last(layer_name, model): # pragma: no cover
    """Move the input channel to the last dim
    :param layer_name: Layer name
    :return: The reshaped weight."""
    layer = get_module(model, layer_name)
    if layer.__class__.__name__ == "WrapperLayer":
        layer = layer.orig_layer

    weight = layer.weight  ##TODO oc*ic, support transposed conv
    if len(weight.shape) == 4:
        weight = weight.permute(0, 2, 3, 1)
        weight = weight.reshape(-1, weight.shape[-1])
    return weight


TUNERS = {}


def register_autotune(name): # pragma: no cover
    """Class decorator to register a smoothquant auto-tune subclass.

    :return: the class of register
    """

    def register(auto_tune):
        TUNERS[name] = auto_tune
        return auto_tune

    return register


class Calibration:
    def __init__(self, model, dataloder=None, q_func=None, device="cpu"):
        self.model = model
        self.dataloader = dataloder
        self.q_func = q_func
        self.device = device

    @torch.no_grad()
    def _save_input_pc_hook(self, name):
        """A forward hook to save input max of a module
        :param name: the module name
        :return: A hook function."""

        def save_input_hook(module, inputs, outputs):
            input = inputs[0]
            ##TODO check input channel is correct
            if len(module.weight.shape) == 4:  ##conv3d or conv1d not supported now, need better way
                input = input.permute(0, 2, 3, 1)
            input = input.reshape(-1, input.shape[-1])
            max_tensor = torch.max(input, dim=0)[0]
            min_tensor = torch.min(input, dim=0)[0]
            if name not in self.input_maxes.keys():
                self.input_mins[name], self.input_maxes[name] = min_tensor, max_tensor
            else:
                self.input_mins[name] = torch.min(self.input_mins[name], min_tensor)
                self.input_maxes[name] = torch.max(self.input_maxes[name], max_tensor)

        return save_input_hook

    @torch.no_grad()
    def _add_min_max_observer(self, modules):
        """
        :param modules: the modules which the observer will insert to
        :return:
        """
        self.hook_handles = []
        for key in modules.keys():
            hook_func = self._save_input_pc_hook(key)
            hook_handle = modules[key].register_forward_hook(hook_func)
            self.hook_handles.append(hook_handle)

    @torch.no_grad()
    def _remove_observer(self):
        """Remove the observer from the model
        :return:"""
        for hook_handle in self.hook_handles:
            hook_handle.remove()

    @torch.no_grad()
    def _dump_min_max(self, calib_iter=100):
        """Dump min max per channel information, the min max value will be saved in input_maxes attribute
        :param calibration_method: only support min_max currently
        :param calib_iter: Sample size for calibration
        :return:"""
        logger.info("Calibrating...")
        if self.q_func:
            self.q_func(self.model)
        else:
            assert self.dataloader, "Please set dataloader for calibration."
            model_forward(self.model, self.dataloader, calib_iter, self.device)

    @torch.no_grad()
    def calibrate(self, calib_iter, op_types=[torch.nn.Conv2d, torch.nn.Linear]):  ##TODO transformers.conv1d
        """
        :param absorb_to_layer: A dict,key is the absorb layer, val is a list of the to be smoothed layer
        :param calib_iter: Data size for calibration
        :return: A dict that saved the layer name and the channel-wise max value info
        """
        ##hook all the module
        self.input_mins = {}
        self.input_maxes = {}

        hook_modules = {}
        for n, module in self.model.named_modules():
            if isinstance(module, tuple(op_types)):
                hook_modules[n] = module

        self._add_min_max_observer(hook_modules)

        self._dump_min_max(calib_iter=calib_iter)
        self._remove_observer()
        return self.input_mins, self.input_maxes


class CpuInfo(object):
    """Get CPU Info."""

    def __init__(self):
        """Get whether the cpu numerical format is bf16, the number of sockets, cores and cores per socket."""
        self._bf16 = False
        self._vnni = False
        info = cpuinfo.get_cpu_info()
        if "arch" in info and "X86" in info["arch"]:
            cpuid = cpuinfo.CPUID()
            max_extension_support = cpuid.get_max_extension_support()
            if max_extension_support >= 7:
                ecx = cpuid._run_asm(
                    b"\x31\xC9",  # xor ecx, ecx
                    b"\xB8\x07\x00\x00\x00" b"\x0f\xa2" b"\x89\xC8" b"\xC3",  # mov eax, 7  # cpuid  # mov ax, cx  # ret
                )
                self._vnni = bool(ecx & (1 << 11))
                eax = cpuid._run_asm(
                    b"\xB9\x01\x00\x00\x00",  # mov ecx, 1
                    b"\xB8\x07\x00\x00\x00" b"\x0f\xa2" b"\xC3",  # mov eax, 7  # cpuid  # ret
                )
                self._bf16 = bool(eax & (1 << 5))
        if "arch" in info and "ARM" in info["arch"]:  # pragma: no cover
            self._sockets = 1
        else:
            self._sockets = self.get_number_of_sockets()
        self._cores = psutil.cpu_count(logical=False)
        self._cores_per_socket = int(self._cores / self._sockets)

    @property
    def bf16(self):
        """Get whether it is bf16."""
        return self._bf16

    @property
    def vnni(self):
        """Get whether it is vnni."""
        return self._vnni

    @property
    def cores_per_socket(self):
        """Get the cores per socket."""
        return self._cores_per_socket

    def get_number_of_sockets(self) -> int:
        """Get number of sockets in platform."""
        cmd = "cat /proc/cpuinfo | grep 'physical id' | sort -u | wc -l"
        if psutil.WINDOWS:
            cmd = r'wmic cpu get DeviceID | C:\Windows\System32\find.exe /C "CPU"'

        with subprocess.Popen(
            args=cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=False,
        ) as proc:
            proc.wait()
            if proc.stdout:
                for line in proc.stdout:
                    return int(line.decode("utf-8", errors="ignore").strip())
        return 0


class GraphTrace:
    """"""

    def __init__(self):
        self.supported_torch_module_to_aten = {
            "Linear": "aten::linear",
            "Conv2d": "aten::_convolution",
            "ConvTranspose2d": "aten::_convolution",
            "LayerNorm": "aten::layer_norm",
            "BatchNorm2d": "aten::batch_norm",
            "GroupNorm": "aten::group_norm",
            "InstanceNorm2d": "aten::instance_norm",
            "LlamaRMSNorm": "aten::mul",
            "T5LayerNorm": "aten::mul",
            "LPLayerNorm": "aten::layer_norm",  ##mpt_chat
        }

        ##TODO potential bug, need to check only have one bug
        ##TODO, must satisfy af(x)=f(ax),current skip layer may be incomplete
        self.skip_ops_to_find_absorb = ["aten::to", "aten::relu", "aten::leaky_relu", "aten::hardtanh"]

        self.could_absorb_layers = [
            "aten::layer_norm",
            "aten::batch_norm",
            "aten::linear",
            "aten::_convolution",
            "aten::group_norm",
            "aten::instance_norm",
            "aten::mul",
        ]  ##TODO,support more norm

    def trace(self, model, dummy_input):
        traced_model = None
        optimize_numerics = False
        orig_device = str(next(model.parameters()).device)
        if orig_device != "cpu" and orig_device != "meta":  # pragma: no cover
            model = model.to("cpu")
            dummy_input = move_input_to_device(dummy_input, "cpu")
        if isinstance(dummy_input, dict) or isinstance(dummy_input, UserDict):
            try:
                traced_model = torch.jit.trace(
                    model, example_kwarg_inputs=dict(dummy_input), strict=False, check_trace=False
                )
                traced_model = torch.jit.freeze(traced_model.eval(), optimize_numerics=optimize_numerics)
            except Exception as e:
                logger.warning(e)
                logger.warning("Jit trace in GraphTrace failed, absorb layer detection is skipped")
        else:
            try:
                traced_model = torch.jit.trace(model, dummy_input, strict=False)
                traced_model = torch.jit.freeze(traced_model.eval(), optimize_numerics=optimize_numerics)
            except:
                try:
                    traced_model = torch.jit.trace(model, dummy_input[0], strict=False)
                    traced_model = torch.jit.freeze(traced_model.eval(), optimize_numerics=optimize_numerics)
                except Exception as e:
                    logger.warning(e)
                    logger.warning("Jit trace in GraphTrace failed, absorb layer detection is skipped")
        model = model.to(orig_device)
        return traced_model

    def get_nodes(self, traced_model, op_types=["Linear"]):
        if isinstance(op_types, str):
            op_types = [op_types]
        nodes = []
        for node in traced_model.graph.nodes():
            node_type = node.kind()
            for op_type in op_types:
                if node_type == op_type:
                    nodes.append((node, op_type))
                    break
        return nodes

    def get_prev_absorb_layer(self, nodes):
        prev_absorb_layer = []
        for node in nodes:
            parent = get_parent(node)
            while 1:
                if parent.kind() in self.skip_ops_to_find_absorb:
                    parent = get_parent(parent)
                    continue
                if parent.kind() in self.could_absorb_layers:
                    parent_out_kinds = []
                    for val_user in list(parent.outputs())[0].uses():
                        next_node = val_user.user
                        parent_out_kinds.append(next_node.kind())
                    parent_out_kinds = set(parent_out_kinds)
                    parent_out_kinds.discard("aten::size")

                    if parent_out_kinds == parent_out_kinds.intersection(self.could_absorb_layers):
                        prev_absorb_layer.append(parent)
                    elif parent_out_kinds.intersection(self.skip_ops_to_find_absorb):
                        res = self.skip_op_absorb_helper(parent)
                        prev_absorb_layer.append(parent) if res else prev_absorb_layer.append(None)
                    else:  # When parent to multiple ops, sq transformation could be wrong.
                        prev_absorb_layer.append(None)
                else:
                    prev_absorb_layer.append(None)
                break
        return prev_absorb_layer

    def skip_op_absorb_helper(self, parent_node):
        for val_user in list(parent_node.outputs())[0].uses():
            next_node = val_user.user
            if next_node.kind() == "aten::size":
                continue
            elif next_node.kind() in self.could_absorb_layers:
                continue
            elif next_node.kind() in self.skip_ops_to_find_absorb:
                node_res = self.skip_op_absorb_helper(next_node)
                if not node_res:
                    return False
            else:
                return False
        return True

    def mapping_torch_module_to_aten(self, op_types):
        res = []
        for op in op_types:
            if op not in self.supported_torch_module_to_aten.keys():
                logger.warning(f"{op} is not supported in smooth quant, ignoring...")
                continue
            res.append(self.supported_torch_module_to_aten[op])
        res = list(set(res))
        return res

    def _check_valid_conv(self, module):
        """Remove group conv except depthwise conv
        :param module:

        :return:
        """
        if not isinstance(module, torch.nn.Conv2d):
            return True
        if module.groups > 1:
            if module.in_channels == module.out_channels and module.groups == module.in_channels:
                return True
            else:
                return False
        return True

    def get_absorb_to_layer(self, model, example_input, op_types, skip_unsupported_layers=True):
        traced_model = self.trace(model, example_input)
        if traced_model is None:
            return None, None

        aten_op_types = self.mapping_torch_module_to_aten(op_types)
        nodes_types = self.get_nodes(traced_model, aten_op_types)
        nodes = [node_type[0] for node_type in nodes_types]
        nodes_prev_absorb = self.get_prev_absorb_layer(nodes)
        absorb_to_layer = {}
        no_absorb_layers = []
        for index, absorb in enumerate(nodes_prev_absorb):
            if absorb is None:
                no_absorb_layers.append(".".join(nodes[index].scopeName().split("/")[-1].split(".")[1:]))
                continue
            node = nodes[index]
            layer_name = ".".join(node.scopeName().split("/")[-1].split(".")[1:])
            absorb_name = ".".join(absorb.scopeName().split("/")[-1].split(".")[1:])
            if layer_name == "" or absorb_name == "":
                continue
            if absorb_name in absorb_to_layer.keys():
                absorb_to_layer[absorb_name].append(layer_name)
            else:
                absorb_to_layer[absorb_name] = [layer_name]
        if skip_unsupported_layers:
            absorb_to_layer = self.remove_unsupported_layers(model, absorb_to_layer, no_absorb_layers)
        return absorb_to_layer, no_absorb_layers

    def remove_unsupported_layers(self, model, absorb_to_layer, no_absorb_layers):
        res = {}
        for key in absorb_to_layer.keys():
            absorb_layer = get_module(model, key)
            layer_type = absorb_layer.__class__.__name__
            if layer_type not in self.supported_torch_module_to_aten.keys():
                no_absorb_layers.extend(absorb_to_layer[key])
                continue
            supported = True
            for layer_name in absorb_to_layer[key]:
                layer = get_module(model, layer_name)
                layer_type = layer.__class__.__name__
                if (layer_type not in self.supported_torch_module_to_aten.keys()) or not self._check_valid_conv(layer):
                    supported = False
                    no_absorb_layers.extend(absorb_to_layer[key])
                    break
            if supported:
                res[key] = absorb_to_layer[key]
        return res


class SQLinearWrapper(torch.nn.Module):
    def __init__(self, module, input_scale, input_minmax, alpha=0.5, dtype=torch.quint8):
        super().__init__()
        self.register_buffer("input_scale", input_scale)
        self.alpha = alpha
        self.dtype = dtype
        # calculate and only save scale, zero_point to avoid memory usage
        self.scale, self.zero_point = self._calculate_qparams(input_scale, input_minmax, dtype)
        self.add_module("sq_linear", module)
        self._update_sq_linear()
        self.ipex = False  # a flag used for ipex inference

    @property
    def weight(self):
        return self.sq_linear.weight

    def forward(self, X):
        if self.ipex:
            X = self.sq_linear(X)
        else:
            X = torch.mul(X, self.input_scale)
            X = self.sq_linear(X)
        return X

    def _calculate_qparams(self, input_scale, input_minmax, dtype=torch.quint8):
        # calculate scale and zero_point
        if dtype == torch.quint8:
            quant_min, quant_max = 0, 255
        min_val = torch.min(input_minmax[0] * input_scale)
        max_val = torch.max(input_minmax[1] * input_scale)
        # work when min_val bigger than zero.
        min_val_neg = torch.min(min_val, torch.zeros_like(min_val))
        max_val_pos = torch.max(max_val, torch.zeros_like(max_val))
        scale = (max_val_pos - min_val_neg) / float(quant_max - quant_min)
        scale = torch.max(scale, torch.tensor([torch.finfo(torch.float32).eps]))
        zero_point = quant_min - torch.round(min_val_neg / scale).to(torch.int)
        zero_point = torch.clamp(zero_point, quant_min, quant_max)
        return scale, zero_point

    def _get_weight_scale(self):
        # get weight scale and zero_point
        from torch.ao.quantization.observer import default_per_channel_weight_observer

        obs = default_per_channel_weight_observer()
        obs(self.sq_linear.weight)
        scale, _ = obs.calculate_qparams()
        return scale

    def _update_sq_linear(self):
        # remove mul and reset sq_linear for ipex inference
        scale = self.input_scale.view(1, self.input_scale.shape[0])
        with torch.no_grad():
            self.sq_linear.weight /= scale

    def _recover_sq_linear(self):
        # remove mul and reset sq_linear for ipex inference
        scale = self.input_scale.view(1, self.input_scale.shape[0])
        with torch.no_grad():
            self.sq_linear.weight *= scale


class WrapperLayer(torch.nn.Module):
    def __init__(self, layer, input_min, input_max, save_q_input=False):
        super(WrapperLayer, self).__init__()
        self.add_module("orig_layer", layer)  # set orig_layer in get/set_module
        self.quant = False
        self.q_input = None
        self.fp32_output = None
        self.input_max = input_max
        self.input_min = input_min
        self.weight_scale = None
        self.input_scale = None
        self.save_q_input = save_q_input
        self.do_blockwise = False

    def enable_quant(self):
        self.quant = True

    def disable_quant(self):
        self.quant = False

    def update_scale(self, input_scale, weight_scale):
        self.input_scale = input_scale
        self.weight_scale = weight_scale

    ##TODO better tradeoff performance and memory, currently it's too slow
    def q_dq_forward(self, x, input_scale, weight_scale):
        layer_copy = copy.deepcopy(self.orig_layer)
        if weight_scale is not None:
            layer_copy.weight *= weight_scale
        q_dq_weight = quant_dequant_w(layer_copy)
        layer_copy.weight.data.copy_(q_dq_weight)
        if input_scale is None:
            x = quant_dequant_x(x, self.input_min, self.input_max)
        else:
            x = input_scale * x
            x = quant_dequant_x(x, self.input_min * input_scale, self.input_max * input_scale)  ##FIXME
        output = layer_copy(x)
        return output

    def q_dq_forward_blockwise(self, x, input_scale):
        layer_copy = copy.deepcopy(self.orig_layer)
        if input_scale is None:
            x = quant_dequant_x(x, self.input_min, self.input_max)
        else:
            x = input_scale * x
            x = quant_dequant_x(x, self.input_min * input_scale, self.input_max * input_scale)  ##FIXME
        output = layer_copy(x)
        return output

    def forward(self, x):
        if self.quant:
            # self.q_input = x * scale ##save the q_input
            if self.save_q_input:
                self.q_input = x
            if not self.do_blockwise:
                output = self.q_dq_forward(x, self.input_scale, self.weight_scale)
            else:
                output = self.q_dq_forward_blockwise(x, self.input_scale)

        else:
            output = self.orig_layer(x)
        self.output = output
        return output


class TorchSmoothQuant:
    """Fake input channel quantization, for more details please refer to
    [1] SmoothQuant: Accurate and Efficient
    Post-Training Quantization for Large Language Models
    [2] SPIQ: Data-Free Per-Channel Static Input Quantization
    Currently, we only handle the layers whose smooth scale could be absorbed, we will support other layers later.

    We only support inplace mode which means the model weights will be changed, you can call recover function
    to recover the weights if needed
    """

    def __init__(
        self,
        model,
        dataloader=None,
        example_inputs=None,
        q_func=None,
        traced_model=None,
        scale_sharing=True,
        record_max_info=False,
    ):
        """
        :param model: Torch model :param dataloader: Calibration dataloader :param traced_model: A specific model
        shares the same architecture as the model and could be traced by torch.jit. If not supplied, we use model
        instead.
        """
        self.model = model
        if not isinstance(self.model, torch.nn.Module):
            return
        device, dtype = self._get_device()
        self.model = self.model.to(device)
        self.model.eval()
        self.device = device
        self.dtype = dtype
        self.dataloader = dataloader
        self.example_inputs = example_inputs
        self.q_func = q_func
        self.input_maxes = {}
        self.input_mins = {}
        self.input_maxes_abs = {}
        self.traced_model = traced_model
        if self.traced_model is None:
            self.traced_model = self.model
        self.weight_scale_info = {}
        self.absorb_scales_info = {}
        self.scale_sharing = scale_sharing
        self.insert_mul = False
        self.allow_absorb = True
        self.record_max_info = record_max_info
        self.max_value_info = {}  # to record max values for alpha tune
        self.absorb_to_layer = {}
        self.weight_max_lb = 1e-5  ##weight max low bound
        self.weight_scale_dict = {}
        self.sq_scale_info = {}
        self.max_value_info = {}
        self.need_calibration = False

    def _get_device(self):
        """Get the model device
        :return:Model device."""
        for _, p in self.model.named_parameters():
            return p.data.device, p.data.dtype

    def _scale_layer_weight(self, layer_name, scale, alpha=0.5, input_minmax=None):  ##input channel
        """Scale the layer weights at input channel, depthwise conv output channel
        :param layer_name: The layer name
        :param scale: The scale to be multiplied
        :param alpha: alpha for SQLinearWrapper
        :param input_minmax: input_minmax for SQLinearWrapper
        :return:"""
        layer = get_module(self.model, layer_name)
        if self.insert_mul:
            layer = get_module(self.model, layer_name)
            if isinstance(layer, SQLinearWrapper):
                layer._recover_sq_linear()
                set_module(self.model, layer_name, layer.sq_linear)  ##recover
            else:
                new_module = SQLinearWrapper(layer, 1.0 / scale, input_minmax, alpha)
                set_module(self.model, layer_name, new_module)
        elif self.allow_absorb:
            scale = reshape_scale_as_weight(layer, scale)
            layer.weight = torch.nn.Parameter(layer.weight * scale)
        return scale

    def _absorb_scales(self, layer_name, scale):  ##output channel
        """Absorb the scale to the layer at output channel
        :param layer_name: The module name
        :param scale: The scale to be absorbed
        :param alpha_key: The alpha passed to SQLinearWrapper
        :return:"""
        if self.insert_mul or not self.allow_absorb:
            return  # absorb is updated in SQLinearWrapper in def _scale_layer_weight

        ##if self.allow absorb
        layer = get_module(self.model, layer_name)
        if layer.__class__.__name__ == "WrapperLayer":
            layer = layer.orig_layer
        if (
            isinstance(layer, torch.nn.BatchNorm2d)
            or isinstance(layer, torch.nn.GroupNorm)
            or isinstance(layer, torch.nn.InstanceNorm2d)
        ):
            if layer.affine:
                layer.weight *= scale
                layer.bias *= scale
            else:
                layer.affine = True
                weight = torch.ones(layer.num_features, device=self.device, dtype=self.dtype) * scale
                layer.weight = torch.nn.Parameter(weight, requires_grad=False)
                bias = torch.zeros(layer.num_features, device=self.device, dtype=self.dtype)
                layer.bias = torch.nn.Parameter(bias, requires_grad=False)
        elif isinstance(layer, torch.nn.LayerNorm):
            if layer.elementwise_affine:
                layer.weight *= scale
                layer.bias *= scale
            else:
                layer.elementwise_affine = True
                weight = torch.ones(layer.num_features, device=self.device, dtype=self.dtype) * scale
                layer.weight = torch.nn.Parameter(torch.ones(weight, requires_grad=False))
                bias = torch.zeros(layer.num_features, device=self.device, dtype=self.dtype)
                layer.bias = torch.nn.Parameter(bias, requires_grad=False)

        elif isinstance(layer, torch.nn.Conv2d):
            ##the order could not be changed
            if hasattr(layer, "bias") and (layer.bias is not None):
                layer.bias *= scale
            scale = scale.view(scale.shape[0], 1, 1, 1)
            layer.weight *= scale

        elif isinstance(layer, torch.nn.Linear):
            if hasattr(layer, "bias") and (layer.bias is not None):
                layer.bias *= scale
            scale = scale.view(scale.shape[0], 1)
            layer.weight *= scale

        elif layer.__class__.__name__ == "LlamaRMSNorm" or layer.__class__.__name__ == "T5LayerNorm":  ##quite tricky
            layer.weight *= scale

        else:
            logger.warning(
                f"found unsupported layer {type(layer)}, try to multiply scale to "
                f"weight and bias directly, this may introduce accuracy issue, please have a check "
            )
            if hasattr(layer, "weight") and layer.weight is not None:
                layer.weight *= scale
            if hasattr(layer, "bias") and layer.bias is not None:
                layer.bias *= scale

    def _export_sq_info(self, absorb_to_layer, input_maxes, alpha=0.5):
        absorb_to_input_maxes = {}
        for key in absorb_to_layer.keys():
            layer_name = absorb_to_layer[key][0]
            absorb_to_input_maxes[key] = input_maxes[layer_name]

        for index, key in enumerate(absorb_to_layer.keys()):
            alpha_tmp = alpha[key] if isinstance(alpha, dict) else alpha
            layer_names = absorb_to_layer[key]
            weights = []
            for layer_name in layer_names:
                weight = reshape_in_channel_to_last(layer_name, self.model)
                weights.append(weight)
            weight_max_per_channel = torch.max(torch.abs(torch.cat(weights, dim=0)), dim=0)[0]

            weight_max_per_channel = weight_max_per_channel.clamp(min=self.weight_max_lb)

            input_max = absorb_to_input_maxes[key]
            layer_names = absorb_to_layer[key]
            # weight_scale = cal_scale(input_max, weights, alpha_tmp)
            input_minmax = [self.input_mins[layer_names[0]].to("cpu"), self.input_maxes[layer_names[0]].to("cpu")]
            abs_input_max = torch.max(torch.abs(input_minmax[0]), torch.abs(input_minmax[1]))
            input_power = torch.pow(abs_input_max, alpha_tmp)
            weight_power = torch.pow(weight_max_per_channel, 1 - alpha_tmp)
            weight_scale = torch.clip(input_power / weight_power, min=1e-5)

            input_scale = 1.0 / weight_scale

            self.max_value_info[key] = {
                "alpha": alpha_tmp,
                "input_minmax": input_minmax,
                "weight_max": weight_max_per_channel,
                "absorbed_layer": layer_names,
            }  # max_value_info is used for pytorch backend and sq_scale_info is used for ipex backend.
            # the input of layers with same absorb layer is the same.
            for op_name in layer_names:
                module = copy.deepcopy(get_module(self.model, op_name))
                new_module = SQLinearWrapper(module, 1.0 / weight_scale, input_minmax, alpha_tmp)
                self.sq_scale_info[op_name] = {}
                self.sq_scale_info[op_name] = {
                    "alpha": alpha_tmp,
                    "input_scale_for_mul": input_scale.to("cpu"),
                    "input_scale_after_mul": new_module.scale,
                    "input_zero_point_after_mul": new_module.zero_point,
                    "input_dtype": new_module.dtype,
                    "weight_scale_after_mul": new_module._get_weight_scale(),
                }

    def _cal_scales(self, absorb_to_layer, input_maxes, alpha=0.5):
        """Cal the adjust scales
        :param absorb_to_layer: A dict mapping absorb layer to smooth quantized layer
        :param input_maxes: The channel-wise input max info for layers
        :param alpha: Alpha value to balance the quantization difficulty of activation and weight, a float of a dict
        :return:"""
        absorb_to_input_maxes = {}
        for key in absorb_to_layer.keys():
            layer_name = absorb_to_layer[key][0]
            absorb_to_input_maxes[key] = input_maxes[layer_name]

        weight_scales_info = {}
        absorb_scales_info = {}
        for index, key in enumerate(absorb_to_layer.keys()):
            alpha_tmp = alpha[key] if isinstance(alpha, dict) else alpha

            input_max = absorb_to_input_maxes[key]
            layer_names = absorb_to_layer[key]
            weights = []
            for layer_name in layer_names:
                weight = reshape_in_channel_to_last(layer_name, self.model)
                weights.append(weight)
            scale = cal_scale(input_max, weights, alpha_tmp)
            absorb_scales_info[key] = 1.0 / scale
            absorb_scales_info[key][scale == 0] = 0
            layer_names = absorb_to_layer[key]
            for layer_name in layer_names:
                ##self._scale_layer_weight(layer_name, scale)
                weight_scales_info[layer_name] = scale
        return absorb_scales_info, weight_scales_info

    def _adjust_parameters(self, absorb_to_layer, input_maxes, alpha=0.5):
        """Adjust the weights and biases
        :param absorb_to_layer: A dict mapping absorb layer to smooth quantized layer
        :param input_maxes: The channel-wise input max info for layers
        :param alpha: Alpha value to balance the quantization difficulty of activation and weight, a float of a dict
        :return:"""
        absorb_scales_info, weight_scales_info = self._cal_scales(absorb_to_layer, input_maxes, alpha)
        if not absorb_scales_info or not weight_scales_info:
            return weight_scales_info, absorb_scales_info
        for index, key in enumerate(absorb_to_layer.keys()):
            if isinstance(alpha, float):
                alpha_tmp = alpha
            elif isinstance(alpha, dict):
                alpha_tmp = alpha[key]
            absorb_scale = absorb_scales_info[key]
            self._absorb_scales(key, absorb_scale)
            layer_names = absorb_to_layer[key]
            for layer_name in layer_names:
                input_minmax = [self.input_mins[layer_names[0]], self.input_maxes[layer_names[0]]]
                self._scale_layer_weight(layer_name, weight_scales_info[layer_name], alpha_tmp, input_minmax)
        return weight_scales_info, absorb_scales_info

    def _check_need_calibration(self, alpha, percentile, op_types, scales_per_op, calib_iter):
        """
        check need calibration or not
        :param alpha: current alpha
        :param percentile: current percentile
        :param op_types: current op_types
        :param scales_per_op: current scales_per_op
        :param calib_iter:: current scales_per_op
        :return:
        """
        need_calib = True
        from peft import PeftModel

        is_peft, is_auto = isinstance(self.model, PeftModel), alpha == "auto"
        if len(self.input_maxes) == 0:  ## the first time
            need_calib = True
            self.alpha = alpha
            self.percentile = percentile
            self.op_types = op_types
            self.scales_per_op = scales_per_op
            self.calib_iter = calib_iter
            return False if (is_auto and not is_peft) else need_calib

        if (
            self.percentile == percentile
            and self.op_types == op_types
            and self.scales_per_op == scales_per_op
            and self.calib_iter == calib_iter
        ):
            if isinstance(alpha, float) or self.alpha == "auto":
                need_calib = False

        self.alpha, self.percentile, self.calib_iter = alpha, percentile, calib_iter
        self.op_types, self.scales_per_op = op_types, scales_per_op
        return need_calib

    @torch.no_grad()
    def _parse_absorb_to_layers(self, op_types, folding):
        str_op_types = [i.__name__ for i in op_types]
        self_absorb_layers = {}
        if self.insert_mul:
            self_absorb_layers = self._get_all_layer_names(op_types)  # TODO: only support linear now.
            # fetch modules with the same input
            group_modules = self._trace(str_op_types, skip_unsupported_layers=False)
            if group_modules is not None:
                # use one input for qkv
                for k, v in group_modules.items():
                    for i in v:
                        if i in self_absorb_layers:
                            self_absorb_layers.pop(i)
                    self_absorb_layers[v[0]] = v
                logger.debug(f"self_absorb_layers:{self_absorb_layers}")
        if self.allow_absorb:
            self.absorb_to_layer, no_absorb_layers = self._trace(str_op_types)
            if self.absorb_to_layer is None and no_absorb_layers is None:
                return None

        # remove self.self_absorb_layers if it exists in self.absorb_to_layer
        for k, v in self.absorb_to_layer.items():
            for i in v:
                if i in self_absorb_layers:
                    self_absorb_layers.pop(i)
        self.absorb_to_layer.update(self_absorb_layers)

        if self.absorb_to_layer is None and no_absorb_layers is None:
            logger.warning(
                "sorry, could not trace the model, smooth quant is ignored."
                "If you are using huggingface model,"
                "you could set torchscript to True "
            )
            return None

        # Check if input_maxes match self.absorb_to_layer
        # (due to self._get_all_layer_names use layer tree instead of forward_path)
        if not folding and self.need_calibration:
            if len(self.input_mins) == 0:  ##there are some modules not used in forward
                calib = Calibration(self.model, self.dataloader, self.q_func, self.device)  ##
                input_mins, input_maxes = calib.calibrate(
                    1, op_types
                )  ##TODO if using qfunc for calibration, it will calibrate twice
            # use qfunc to calibrate, the input min could be used for fixed alpha transformation
            self.input_mins = input_mins
            self.input_maxes = input_maxes
            diff_modules = set(self.absorb_to_layer.keys()).difference(input_mins.keys())
            for d in diff_modules:
                del self.absorb_to_layer[d]
        return self.absorb_to_layer

    @torch.no_grad()
    def transform(
        self,
        alpha=0.5,
        folding=False,
        percentile=100,
        op_types=[torch.nn.Linear, torch.nn.Conv2d],
        scales_per_op=False,
        calib_iter=100,
        weight_clip=True,
        scale_sharing=True,
        auto_alpha_args={
            "init_alpha": 0.5,
            "alpha_min": 0.0,
            "alpha_max": 1.0,
            "alpha_step": 0.1,
            "shared_criterion": "mean",
            "n_samples": 32,  ##512 for cuda, 128 for cpu?
        },
    ):
        """The main entry of smooth quant
        :param alpha: Alpha value to balance the quantization difficulty of activation and weight, please refer
        to the paper for more details
        :param folding: whether insert mul(False) or just allow foldable layers(True) for SmoothQuant
        :param percentile: Not supported now
        :param op_types: The op typed to be smooth quantized
        :param scales_per_op: Not supported now
        :param calib_iter: Data size for calibration
        :param weight_clip: Whether to clip weight_max when calculating scales.

        :param auto_alpha_args: Hyperparameters used to set the alpha search space in SQ auto-tuning.
            By default, the search space is 0.0-1.0 with step_size 0.1.
            do_blockwise: Whether to do blockwise auto-tuning.
        :param init_alpha: A hyperparameter that is used in SQ auto-tuning; by default it is 0.5.
        :return: A FP32 model with the same architecture as the orig model but with different weight which will be
        benefit to quantization.
        """

        if not isinstance(self.model, torch.nn.Module):
            logger.warning("smoothquant is ignored since the model is not a torch module")
            return self.model

        if isinstance(alpha, float) and (alpha < 0):
            logger.warning("reset alpha to >=0")
            alpha = numpy.clip(alpha, 0.0)

        if folding:
            self.insert_mul, self.allow_absorb = False, True
        else:
            self.insert_mul, self.allow_absorb = True, False
        self.weight_clip = weight_clip

        self.revert()
        self.need_calibration = self._check_need_calibration(alpha, percentile, op_types, scales_per_op, calib_iter)
        with torch.no_grad():
            str_op_types = [i.__name__ for i in op_types]
            input_maxes_abs = self.input_maxes_abs
            if self.need_calibration:  ##avoid multiple calibaration during tuning if the only difference is alpha
                if self.insert_mul:
                    self.self_absorb_layers = self._get_all_layer_names(op_types)  # TODO: only support linear now.
                    if self.scale_sharing:
                        # fetch modules with the same input
                        group_modules = self._trace(str_op_types, skip_unsupported_layers=False)
                        if group_modules is not None:
                            # use one input for qkv
                            for k, v in group_modules.items():
                                for i in v:
                                    if i in self.self_absorb_layers:
                                        self.self_absorb_layers.pop(i)
                                self.self_absorb_layers[v[0]] = v
                            logger.debug(f"self_absorb_layers:{self.self_absorb_layers}")

        self.absorb_to_layer = self._parse_absorb_to_layers(
            op_types, folding
        )  ##need to forward to check modules not used in forward
        if len(self.input_mins) != 0:  ##this is from _parse_absorb_to_layers, ugly code to support q_func
            input_maxes_abs = {}
            for key in self.input_mins.keys():
                input_maxes_abs[key] = torch.max(torch.abs(self.input_mins[key]), torch.abs(self.input_maxes[key]))
            if self.q_func:
                self.need_calibration = False  # Avoid double-calibration in fixed-value alpha SQ.

        if self.absorb_to_layer is None:
            logger.warning("empty absorb_to_layer, smoothquant is ignored ")
            return self.model
        example_inputs = self._get_example_input()
        if alpha == "auto":  ##TODO need to polish later
            auto_alpha_version = "version1"
            auto_alpha_tuner = TUNERS[auto_alpha_version](
                self.model,
                self.dataloader,
                self.absorb_to_layer,
                op_types=op_types,
                device=self.device,
                q_func=self.q_func,
                folding=folding,
                example_inputs=self.example_inputs,
                **auto_alpha_args,
            )
            self.alpha = auto_alpha_tuner.tune()
            input_maxes_abs = auto_alpha_tuner.input_maxes_abs
            self.input_mins, self.input_maxes = auto_alpha_tuner.input_mins, auto_alpha_tuner.input_maxes
            if auto_alpha_tuner.loss_type == "blockwise":
                self.block_names = auto_alpha_tuner.block_names

        elif self.need_calibration:
            calib = Calibration(self.model, self.dataloader, self.q_func, self.device)
            self.input_mins, self.input_maxes = calib.calibrate(calib_iter, op_types)
            input_maxes_abs = {}
            for key in self.input_mins.keys():
                input_maxes_abs[key] = torch.max(torch.abs(self.input_mins[key]), torch.abs(self.input_maxes[key]))

        if example_inputs is not None:
            out_pre_sq = model_forward_per_sample(self.model, example_inputs, self.device)

        if folding:
            self._save_scale = False  ##TODO remove it later

        if self.record_max_info:
            self._export_sq_info(self.absorb_to_layer, input_maxes_abs, self.alpha)
            # # max_info is recorded in self.max_value_info
            # self._adjust_parameters(self.absorb_to_layer, input_maxes_abs, alpha)
            self.model._smoothquant_optimized = False
            return self.model

        self.weight_scale_info, self.absorb_scales_info = self._adjust_parameters(
            self.absorb_to_layer, input_maxes_abs, self.alpha
        )
        self.model._smoothquant_optimized = True

        if example_inputs is not None:
            # Check mathematical equivalency
            out_post_sq = model_forward_per_sample(self.model, example_inputs, self.device)
            if not self.output_is_equal(out_post_sq, out_pre_sq):
                logger.warning(
                    "Mathematical equivelancy of Smoothquant is not preserved. "
                    "Please kindly report this issue to https://github.com/intel/neural-compressor."
                )
        else:
            logger.warning(" Could not get example input, equivelancy check is skipped")

        return self.model

    def output_is_equal(self, out1, out2, atol=1e-04):
        try:
            if isinstance(out1, tuple):
                return all(torch.all(torch.isclose(out1[i], out2[i], atol=atol)) for i in range(len(out1)))
            elif isinstance(out1, dict):
                return all(torch.all(torch.isclose(out1[k], out2[k], atol=atol)) for k in out1.keys())
            elif isinstance(out1, torch.Tensor):
                return torch.all(torch.isclose(out1, out2, atol=atol))
            return False
        except:
            logger.warning(
                "Automatically check failed, Please check equivelancy manually "
                "between out_pre_sq and out_post_sq if necessary."
            )
            return True

    @torch.no_grad()
    def revert(self):
        """Revert the model weights
        :return:"""
        for key in self.weight_scale_info:
            self._scale_layer_weight(key, 1.0 / self.weight_scale_info[key])
        for key in self.absorb_scales_info:
            self._absorb_scales(key, 1.0 / self.absorb_scales_info[key])
        self.weight_scale_info = {}  ##clear the data
        self.absorb_scales_info = {}

    def _get_all_layer_names(self, op_types=[torch.nn.Linear]):
        """Try the model to find the layers which can be smooth quantized.

        :param op_types: The op types to be smooth quantized
        :return:
        self_absorb_layer: A dict, absorb layer name (itself): layers to be smooth quantized
        """
        self_absorb_layer = {}
        op_types = [torch.nn.Linear]  # TODO： only support SQLinearWrapper
        for name, module in self.model.named_modules():
            if isinstance(module, tuple(op_types)):
                self_absorb_layer[name] = [name]
        return self_absorb_layer

    def _get_example_input(self):
        if self.dataloader is None and self.example_inputs is None:
            return None
        if self.example_inputs is None:
            try:
                for idx, (input, label) in enumerate(self.dataloader):
                    self.example_inputs = input
                    break
            except:
                for idx, input in enumerate(self.dataloader):
                    self.example_inputs = input
                    break

        return self.example_inputs

    def _trace(self, op_types, skip_unsupported_layers=True):
        """Try the model to find the layers which can be smooth quantized.

        :param op_types: The op types to be smooth quantized
        :return:
        absorb_to_layer: A dict, absorb layer name:layers to be smooth quantized
        no_absorb_layers: A list saving the layers which could not find the absorb layer
        """

        tg = GraphTrace()
        self._get_example_input()
        absorb_to_layer, no_absorb_layers = tg.get_absorb_to_layer(
            self.traced_model,
            self.example_inputs,
            op_types,
            skip_unsupported_layers=skip_unsupported_layers,
        )
        if not skip_unsupported_layers:
            return absorb_to_layer
        if absorb_to_layer is None and no_absorb_layers is None:
            logger.warning(
                "sorry, could not trace the model, smooth quant is skipped."
                "If you are using huggingface model,"
                "you could set torchscript to True "
                "when loading the model or set the return_dict to False"
            )
        elif absorb_to_layer == {}:
            logger.warning("could not find any layer to be absorbed")
        else:
            to_absorb_cnt = 0
            for key, item in absorb_to_layer.items():
                to_absorb_cnt += len(item)
            logger.info(
                f" {to_absorb_cnt} out of {to_absorb_cnt + len(no_absorb_layers)} "
                f"layers could be absorbed in smooth quant"
            )
        return absorb_to_layer, no_absorb_layers
