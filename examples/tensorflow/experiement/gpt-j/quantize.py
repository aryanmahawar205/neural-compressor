#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Intel Corporation
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
#

#

#!/usr/bin/env python
# coding=utf-8
# Copyright 2021 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import math
from dataclasses import dataclass, field
from itertools import chain
from typing import Optional
import time
import numpy as np
import datasets
import tensorflow as tf
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from collections import defaultdict

import transformers
from transformers import (
    TF_MODEL_FOR_CAUSAL_LM_MAPPING,
    AutoConfig,
    AutoTokenizer,
    HfArgumentParser,
    TFAutoModelForCausalLM,
    TFTrainingArguments,
    set_seed,
)
from transformers.utils.versions import require_version


logger = logging.getLogger(__name__)
require_version("datasets>=1.8.0", "To fix: pip install -r benchmarks/language_modeling/tensorflow/gpt_j/requirements.txt")
MODEL_CONFIG_CLASSES = list(TF_MODEL_FOR_CAUSAL_LM_MAPPING.keys())
MODEL_TYPES = tuple(conf.model_type for conf in MODEL_CONFIG_CLASSES)

@dataclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to use.
    """

    model_name_or_path: Optional[str] = field(
        default="EleutherAI/gpt-j-6B",
        metadata={
            "help": (
                "The model checkpoint for GPT-J weights."
            )
        },
    )
    config_overrides: Optional[str] = field(
        default=None,
        metadata={
            "help": (
                "Override some existing default config settings when a model is trained from scratch. Example: "
                "n_embd=10,resid_pdrop=0.2,scale_attn_weights=false,summary_type=cls_index"
            )
        },
    )
    checkpoint: Optional[str] = field(
        default=None,
        metadata={"help": "Where do you want to store the pretrained models downloaded from huggingface.co"},
    )
    use_fast_tokenizer: bool = field(
        default=True,
        metadata={"help": "Whether to use one of the fast tokenizer (backed by the tokenizers library) or not."},
    )
    precision: Optional[str] = field(
        default="fp32",
        metadata={"help": "The precision that we want to run with."},
    )



@dataclass
class DataTrainingArguments:
    """
    Arguments pertaining to what data we are going to input our model for evaluation.
    """

    dataset_name: Optional[str] = field(
        default="EleutherAI/lambada_openai", metadata={"help": "The name of the dataset to use (via the datasets library)."}
    )
    dataset_config_name: Optional[str] = field(
        default=None, metadata={"help": "The configuration name of the dataset to use (via the datasets library)."}
    )
    block_size: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "Optional input sequence length after tokenization. "
                "The training dataset will be truncated in block of this size for training. "
                "Default to the model max input length for single sentence inputs (take into account special tokens)."
            )
        },
    )
    preprocessing_num_workers: Optional[int] = field(
        default=None,
        metadata={"help": "The number of processes to use for the preprocessing."},
    )

parser = HfArgumentParser((ModelArguments, DataTrainingArguments, TFTrainingArguments))
model_args, data_args, run_args = parser.parse_args_into_dataclasses()

logger.setLevel(logging.INFO)
datasets.utils.logging.set_verbosity_warning()
transformers.utils.logging.set_verbosity_info()

if run_args.seed is not None:
    set_seed(run_args.seed)

raw_datasets = load_dataset(
        data_args.dataset_name,
        data_args.dataset_config_name,
        cache_dir=model_args.checkpoint,
        use_auth_token=None,
    )
    
config = AutoConfig.from_pretrained(model_args.model_name_or_path)
tokenizer = AutoTokenizer.from_pretrained(model_args.model_name_or_path)
column_names = raw_datasets["test"].column_names
text_column_name = "text" if "text" in column_names else column_names[0]

mydata = tokenizer(raw_datasets["test"][text_column_name], return_tensors="np").input_ids

marg = {}
stacked = np.concatenate(mydata)
unique, counts = np.unique(stacked, return_counts=True)
counts = counts / np.sum(counts)

marg = dict(zip(unique, counts))
marg = defaultdict(lambda: 0, marg)

def prepare_attention_mask_for_generation(
    inputs: tf.Tensor,
    pad_token_id=50256,
    eos_token_id=50256,
) -> tf.Tensor:
    is_input_ids = len(inputs.shape) == 2 and inputs.dtype in (tf.int32, tf.int64)
    is_pad_token_in_inputs = (pad_token_id is not None) and tf.math.reduce_any(inputs == pad_token_id)
    is_pad_token_not_equal_to_eos_token_id = (eos_token_id is None) or (pad_token_id != eos_token_id)

    # Check if input is input_ids and padded -> only then is attention_mask defined
    if is_input_ids and is_pad_token_in_inputs and is_pad_token_not_equal_to_eos_token_id:
        return tf.cast(tf.math.not_equal(inputs, pad_token_id), dtype=tf.int32)
    else:
        return tf.ones(inputs.shape[:2], dtype=tf.int32)

def evaluate(model, iter, tf_eval_dataset=mydata):
    if isinstance(model, str):
        model = tf.saved_model.load(model)
    infer = model.signatures["serving_default"]
    batch_size = 1
    warmup = 5
    iteration = None
    latency_list = []
    iteration = iter
    correct = 0
    pad_token_id = 50256
    for idx, data in enumerate(tf_eval_dataset):
        print('Running Iteration: ', idx)
        input_ids = tf.convert_to_tensor([data[:-1]], dtype=tf.int32)
        cur_len = len(data)-1
        input_ids_padding = tf.ones((batch_size, 1), dtype=tf.int32) * (pad_token_id or 0)
        generated = tf.concat([input_ids, input_ids_padding], axis=-1)
        input_ids = generated[:, :cur_len]
        attention_mask = prepare_attention_mask_for_generation(input_ids)
        inputs = {'input_ids': input_ids, 'attention_mask': attention_mask}

        start = time.time()
        predictions = infer(**inputs)
        end = time.time()

        dur = end-start
        print('Time taken: ', dur)
        latency_list.append(dur)
        if idx >= iteration:
            break
    latency = np.array(latency_list[warmup:]).mean() / 1
    acc = correct/(iteration+1)
    return latency, acc

def main():    
    with run_args.strategy.scope():
        model = TFAutoModelForCausalLM.from_pretrained(model_args.model_name_or_path, config=config)
        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.OFF
        from convert import ConvertSavedModel
        from configs import op_wise_config_matmul, int8_sequences
        converter = ConvertSavedModel(src='./gpt-j-6B', 
                                      dst='./converted_gpt-j-6B', 
                                      evaluate=evaluate,
                                      op_wise_config=op_wise_config_matmul,
                                      int8_sequences=int8_sequences)
        converter()

if __name__ == "__main__":
    main()