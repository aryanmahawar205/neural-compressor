# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors and The HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
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
""" Finetuning the library models for question-answering on SQuAD (DistilBERT, Bert, XLM, XLNet)."""

from __future__ import absolute_import, division, print_function
from transformers.data.processors.squad import SquadV1Processor, SquadV2Processor, SquadResult
from transformers.data.metrics.squad_metrics import compute_predictions_logits, compute_predictions_log_probs, squad_evaluate

import argparse
import logging
import os
import random
import glob
import timeit
import numpy as np
import torch
from torch.utils.data import (DataLoader, RandomSampler, SequentialSampler, TensorDataset)
from torch.utils.data.distributed import DistributedSampler

from torch.quantization import quantize, prepare, convert, propagate_qconfig_, add_observer_
from torch.quantization import \
    QuantWrapper, QuantStub, DeQuantStub, default_qconfig, default_per_channel_qconfig

from tqdm import tqdm, trange

from transformers import (WEIGHTS_NAME, BertConfig,
                                  BertForQuestionAnswering, BertTokenizer,
                                  XLMConfig, XLMForQuestionAnswering,
                                  XLMTokenizer, XLNetConfig,
                                  XLNetForQuestionAnswering,
                                  XLNetTokenizer,
                                  DistilBertConfig, DistilBertForQuestionAnswering, DistilBertTokenizer,
                                  AlbertConfig, AlbertForQuestionAnswering, AlbertTokenizer,
                                  XLMConfig, XLMForQuestionAnswering, XLMTokenizer,
                                  )

from transformers import AdamW, get_linear_schedule_with_warmup, squad_convert_examples_to_features

logger = logging.getLogger(__name__)

ALL_MODELS = sum((tuple(conf.pretrained_config_archive_map.keys()) \
                  for conf in (BertConfig, XLNetConfig, XLMConfig)), ())

MODEL_CLASSES = {
    'bert': (BertConfig, BertForQuestionAnswering, BertTokenizer),
    'xlnet': (XLNetConfig, XLNetForQuestionAnswering, XLNetTokenizer),
    'xlm': (XLMConfig, XLMForQuestionAnswering, XLMTokenizer),
    'distilbert': (DistilBertConfig, DistilBertForQuestionAnswering, DistilBertTokenizer),
    'albert': (AlbertConfig, AlbertForQuestionAnswering, AlbertTokenizer),
    'xlm': (XLMConfig, XLMForQuestionAnswering, XLMTokenizer)
}

def set_seed(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.n_gpu > 0:
        torch.cuda.manual_seed_all(args.seed)

def to_list(tensor):
    return tensor.detach().cpu().tolist()

def train(args, train_dataset, model, tokenizer):
    """ Train the model """
    try:
        from torch.utils.tensorboard import SummaryWriter
    except ImportError:
        from tensorboardX import SummaryWriter

    if args.local_rank in [-1, 0]:
        tb_writer = SummaryWriter()

    args.train_batch_size = args.per_gpu_train_batch_size * max(1, args.n_gpu)
    train_sampler = RandomSampler(train_dataset) if args.local_rank == -1 else DistributedSampler(train_dataset)
    train_dataloader = DataLoader(train_dataset, sampler=train_sampler, batch_size=args.train_batch_size)

    if args.max_steps > 0:
        t_total = args.max_steps
        args.num_train_epochs = args.max_steps // (len(train_dataloader) // args.gradient_accumulation_steps) + 1
    else:
        t_total = len(train_dataloader) // args.gradient_accumulation_steps * args.num_train_epochs

    # Prepare optimizer and schedule (linear warmup and decay)
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': args.weight_decay},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate, eps=args.adam_epsilon)
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=args.warmup_steps, num_training_steps=t_total)

    if args.fp16:
        try:
            from apex import amp
        except ImportError:
            raise ImportError("Please install apex from https://www.github.com/nvidia/apex to use fp16 training.")

        model, optimizer = amp.initialize(model, optimizer, opt_level=args.fp16_opt_level)

    # multi-gpu training (should be after apex fp16 initialization)
    if args.n_gpu > 1:
        model = torch.nn.DataParallel(model)

    # Distributed training (should be after apex fp16 initialization)
    if args.local_rank != -1:
        model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[args.local_rank],
                                                          output_device=args.local_rank,
                                                          find_unused_parameters=True)

    # Train!
    logger.info("***** Running training *****")
    logger.info("  Num examples = %d", len(train_dataset))
    logger.info("  Num Epochs = %d", args.num_train_epochs)
    logger.info("  Instantaneous batch size per GPU = %d", args.per_gpu_train_batch_size)
    logger.info("  Total train batch size (w. parallel, distributed & accumulation) = %d",
                   args.train_batch_size * args.gradient_accumulation_steps * (torch.distributed.get_world_size() if args.local_rank != -1 else 1))
    logger.info("  Gradient Accumulation steps = %d", args.gradient_accumulation_steps)
    logger.info("  Total optimization steps = %d", t_total)

    global_step = 1
    tr_loss, logging_loss = 0.0, 0.0
    model.zero_grad()
    train_iterator = trange(int(args.num_train_epochs), desc="Epoch", disable=args.local_rank not in [-1, 0])
    set_seed(args)  # Added here for reproductibility (even between python 2 and 3)

    for _ in train_iterator:
        epoch_iterator = tqdm(train_dataloader, desc="Iteration", disable=args.local_rank not in [-1, 0])
        for step, batch in enumerate(epoch_iterator):
            model.train()
            batch = tuple(t.to(args.device) for t in batch)

            inputs = {
                'input_ids':       batch[0],
                'attention_mask':  batch[1],
                'start_positions': batch[3],
                'end_positions':   batch[4]
            }

            if args.model_type != 'distilbert':
                inputs['token_type_ids'] = None if args.model_type == 'xlm' else batch[2]

            if args.model_type in ['xlnet', 'xlm']:
                inputs.update({'cls_index': batch[5], 'p_mask': batch[6]})

            outputs = model(**inputs)
            loss = outputs[0]  # model outputs are always tuple in transformers (see doc)

            if args.n_gpu > 1:
                loss = loss.mean() # mean() to average on multi-gpu parallel (not distributed) training
            if args.gradient_accumulation_steps > 1:
                loss = loss / args.gradient_accumulation_steps

            if args.fp16:
                with amp.scale_loss(loss, optimizer) as scaled_loss:
                    scaled_loss.backward()
            else:
                loss.backward()

            tr_loss += loss.item()
            if (step + 1) % args.gradient_accumulation_steps == 0:
                if args.fp16:
                    torch.nn.utils.clip_grad_norm_(amp.master_params(optimizer), args.max_grad_norm)
                else:
                    torch.nn.utils.clip_grad_norm_(model.parameters(), args.max_grad_norm)

                optimizer.step()
                scheduler.step()  # Update learning rate schedule
                model.zero_grad()
                global_step += 1

                # Log metrics
                if args.local_rank in [-1, 0] and args.logging_steps > 0 and global_step % args.logging_steps == 0:
                    if args.local_rank == -1 and args.evaluate_during_training:  # Only evaluate when single GPU otherwise metrics may not average well
                        results = evaluate(args, model, tokenizer)
                        for key, value in results.items():
                            tb_writer.add_scalar('eval_{}'.format(key), value, global_step)
                    tb_writer.add_scalar('lr', scheduler.get_lr()[0], global_step)
                    tb_writer.add_scalar('loss', (tr_loss - logging_loss)/args.logging_steps, global_step)
                    logging_loss = tr_loss

                # Save model checkpoint
                if args.local_rank in [-1, 0] and args.save_steps > 0 and global_step % args.save_steps == 0:
                    output_dir = os.path.join(args.output_dir, 'checkpoint-{}'.format(global_step))
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    model_to_save = model.module if hasattr(model, 'module') else model  # Take care of distributed/parallel training
                    model_to_save.save_pretrained(output_dir)
                    torch.save(args, os.path.join(output_dir, 'training_args.bin'))
                    logger.info("Saving model checkpoint to %s", output_dir)

            if args.max_steps > 0 and global_step > args.max_steps:
                epoch_iterator.close()
                break
        if args.max_steps > 0 and global_step > args.max_steps:
            train_iterator.close()
            break

    if args.local_rank in [-1, 0]:
        tb_writer.close()

    return global_step, tr_loss / global_step


def evaluate(args, model, tokenizer, prefix="", calibration=False):
    dataset, examples, features = load_and_cache_examples(args, tokenizer, evaluate=True, output_examples=True)

    dataset_cached = "./dataset_cached"
    if not os.path.exists(dataset_cached):
        os.makedirs(dataset_cached)

    args.eval_batch_size = args.per_gpu_eval_batch_size * max(1, args.n_gpu)

    # Note that DistributedSampler samples randomly
    eval_sampler = SequentialSampler(dataset)
    eval_dataloader = DataLoader(dataset, sampler=eval_sampler, batch_size=args.eval_batch_size)

    calibation_iteration = int((len(dataset) * 0.05 + args.eval_batch_size - 1) / args.eval_batch_size)

    # multi-gpu evaluate
    if args.n_gpu > 1:
        model = torch.nn.DataParallel(model)

    # Eval!
    logger.info("***** Running evaluation {} *****".format(prefix))
    logger.info("  Num examples = %d", len(dataset))
    print("  Batch size = %d" % args.eval_batch_size)

    if args.mkldnn_eval:
        from torch.utils import mkldnn as mkldnn_utils
        model = mkldnn_utils.to_mkldnn(model)
        print(model)

    all_results = []
    evalTime = 0
    nb_eval_steps = 0

    for batch in tqdm(eval_dataloader, desc="Evaluating"):
        model.eval()
        batch = tuple(t.to(args.device) for t in batch)

        if calibration and nb_eval_steps >= calibation_iteration:
                break

        with torch.no_grad():
            inputs = {
                'input_ids':      batch[0],
                'attention_mask': batch[1]
            }

            if args.model_type != 'distilbert':
                inputs['token_type_ids'] = None if args.model_type == 'xlm' else batch[2]  # XLM don't use segment_ids

            example_indices = batch[3]

            # XLNet and XLM use more arguments for their predictions
            if args.model_type in ['xlnet', 'xlm']:
                inputs.update({'cls_index': batch[4], 'p_mask': batch[5]})

            if nb_eval_steps >= args.warmup:
                start_time = timeit.default_timer()
            outputs = model(**inputs)

        for i, example_index in enumerate(example_indices):
            eval_feature = features[example_index.item()]
            unique_id = int(eval_feature.unique_id)

            output = [to_list(output[i]) for output in outputs]

            # Some models (XLNet, XLM) use 5 arguments for their predictions, while the other "simpler"
            # models only use two.
            if len(output) >= 5:
                start_logits = output[0]
                start_top_index = output[1]
                end_logits = output[2]
                end_top_index = output[3]
                cls_logits = output[4]

                result = SquadResult(
                    unique_id, start_logits, end_logits, 
                    start_top_index=start_top_index, 
                    end_top_index=end_top_index, 
                    cls_logits=cls_logits
                )

            else:
                start_logits, end_logits = output
                result = SquadResult(
                    unique_id, start_logits, end_logits
                )

            all_results.append(result)

        if nb_eval_steps >= args.warmup:
            evalTime += (timeit.default_timer() - start_time)

        nb_eval_steps += 1

        if args.iter > 0 and nb_eval_steps >= (args.warmup + args.iter):
            break

    if nb_eval_steps >= args.warmup:
        perf = (nb_eval_steps - args.warmup) * args.eval_batch_size / evalTime
        if args.eval_batch_size == 1:
                print('Latency: %.3f ms' % (evalTime / (nb_eval_steps - args.warmup) * 1000))
        print("Evaluation done in total %f secs (Throughput: %f samples/sec)" % (evalTime, perf))
    else:
        logger.info("*****no performance, please check dataset length and warmup number *****")

    # Compute predictions
    output_prediction_file = os.path.join(dataset_cached, "predictions_{}.json".format(prefix))
    output_nbest_file = os.path.join(dataset_cached, "nbest_predictions_{}.json".format(prefix))

    if args.version_2_with_negative:
        output_null_log_odds_file = os.path.join(dataset_cached, "null_odds_{}.json".format(prefix))
    else:
        output_null_log_odds_file = None

    # XLNet and XLM use a more complex post-processing procedure
    if args.model_type in ['xlnet', 'xlm']:
        start_n_top = model.config.start_n_top if hasattr(model, "config") else model.module.config.start_n_top
        end_n_top = model.config.end_n_top if hasattr(model, "config") else model.module.config.end_n_top

        predictions = compute_predictions_log_probs(examples, features, all_results, args.n_best_size,
                        args.max_answer_length, output_prediction_file,
                        output_nbest_file, output_null_log_odds_file,
                        start_n_top, end_n_top,
                        args.version_2_with_negative, tokenizer, args.verbose_logging)
    elif not calibration and args.iter == 0:
        predictions = compute_predictions_logits(examples, features, all_results, args.n_best_size,
                        args.max_answer_length, args.do_lower_case, output_prediction_file,
                        output_nbest_file, output_null_log_odds_file, args.verbose_logging,
                        args.version_2_with_negative, args.null_score_diff_threshold)

    # Compute the F1 and exact scores.
    if not calibration and args.iter == 0:
        results = squad_evaluate(examples, predictions)
        bert_task_acc_keys = ['best_f1', 'f1', 'mcc', 'spearmanr', 'acc']
        for key in bert_task_acc_keys:
            if key in results.keys():
                acc = results[key]
                break
        print("Accuracy: %.5f" % acc)
    else:
        results = None
    return results, perf


def load_and_cache_examples(args, tokenizer, evaluate=False, output_examples=False):
    if args.local_rank not in [-1, 0] and not evaluate:
        torch.distributed.barrier()  # Make sure only the first process in distributed training process the dataset, and the others will use the cache

    # Load data features from cache or dataset file
    input_dir = "./dataset_cached"
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    cached_features_file = os.path.join(input_dir, 'cached_{}_{}_{}'.format(
        'dev' if evaluate else 'train',
        list(filter(None, args.model_name_or_path.split('/'))).pop(),
        str(args.max_seq_length))
    )

    # Init features and dataset from cache if it exists
    if os.path.exists(cached_features_file) and not args.overwrite_cache:
        logger.info("Loading features from cached file %s", cached_features_file)
        features_and_dataset = torch.load(cached_features_file)
        features, dataset, examples = features_and_dataset["features"], features_and_dataset["dataset"], \
            features_and_dataset["examples"] 
    else:
        logger.info("Creating features from dataset file at %s", input_dir)

        if not args.data_dir:
            try:
                import tensorflow_datasets as tfds
            except ImportError:
                raise ImportError("If not data_dir is specified, tensorflow_datasets needs to be installed.")

            if args.version_2_with_negative:
                logger.warn("tensorflow_datasets does not handle version 2 of SQuAD.")

            tfds_examples = tfds.load("squad")
            examples = SquadV1Processor().get_examples_from_dataset(tfds_examples, evaluate=evaluate)
        else:
            processor = SquadV2Processor() if args.version_2_with_negative else SquadV1Processor()
            examples = processor.get_dev_examples(args.data_dir) if evaluate else processor.get_train_examples(args.data_dir)

        features, dataset = squad_convert_examples_to_features( 
            examples=examples,
            tokenizer=tokenizer,
            max_seq_length=args.max_seq_length,
            doc_stride=args.doc_stride,
            max_query_length=args.max_query_length,
            is_training=not evaluate,
            return_dataset='pt'
        )

        if args.local_rank in [-1, 0]:
            logger.info("Saving features into cached file %s", cached_features_file)
            torch.save({"features": features, "dataset": dataset, "examples": examples}, cached_features_file)

    if args.local_rank == 0 and not evaluate:
        torch.distributed.barrier()  # Make sure only the first process in distributed training process the dataset, and the others will use the cache

    if output_examples:
        return dataset, examples, features
    return dataset


def main():
    parser = argparse.ArgumentParser()

    # Required parameters
    parser.add_argument("--model_type", default=None, type=str, required=True,
                        help="Model type selected in the list: " + ", ".join(MODEL_CLASSES.keys()))
    parser.add_argument("--model_name_or_path", default=None, type=str, required=True,
                        help="Path to pre-trained model or shortcut name selected in the list: " + ", ".join(ALL_MODELS))
    parser.add_argument("--output_dir", default=None, type=str, required=True,
                        help="The output directory where the model checkpoints and predictions will be written.")

    # Other parameters
    parser.add_argument("--data_dir", default=None, type=str,
                        help="The input data dir. Should contain the .json files for the task. If not specified, will run with tensorflow_datasets.")
    parser.add_argument("--config_name", default="", type=str,
                        help="Pretrained config name or path if not the same as model_name")
    parser.add_argument("--tokenizer_name", default="", type=str,
                        help="Pretrained tokenizer name or path if not the same as model_name")
    parser.add_argument("--cache_dir", default="", type=str,
                        help="Where do you want to store the pre-trained models downloaded from s3")

    parser.add_argument('--version_2_with_negative', action='store_true',
                        help='If true, the SQuAD examples contain some that do not have an answer.')
    parser.add_argument('--null_score_diff_threshold', type=float, default=0.0,
                        help="If null_score - best_non_null is greater than the threshold predict null.")

    parser.add_argument("--max_seq_length", default=384, type=int,
                        help="The maximum total input sequence length after WordPiece tokenization. Sequences "
                             "longer than this will be truncated, and sequences shorter than this will be padded.")
    parser.add_argument("--doc_stride", default=128, type=int,
                        help="When splitting up a long document into chunks, how much stride to take between chunks.")
    parser.add_argument("--max_query_length", default=64, type=int,
                        help="The maximum number of tokens for the question. Questions longer than this will "
                             "be truncated to this length.")
    parser.add_argument("--do_train", action='store_true',
                        help="Whether to run training.")
    parser.add_argument("--do_eval", action='store_true',
                        help="Whether to run eval on the dev set.")
    parser.add_argument("--evaluate_during_training", action='store_true',
                        help="Rul evaluation during training at each logging step.")
    parser.add_argument("--do_lower_case", action='store_true',
                        help="Set this flag if you are using an uncased model.")

    parser.add_argument("--per_gpu_train_batch_size", default=8, type=int,
                        help="Batch size per GPU/CPU for training.")
    parser.add_argument("--per_gpu_eval_batch_size", default=8, type=int,
                        help="Batch size per GPU/CPU for evaluation.")
    parser.add_argument("--learning_rate", default=5e-5, type=float,
                        help="The initial learning rate for Adam.")
    parser.add_argument('--gradient_accumulation_steps', type=int, default=1,
                        help="Number of updates steps to accumulate before performing a backward/update pass.")
    parser.add_argument("--weight_decay", default=0.0, type=float,
                        help="Weight decay if we apply some.")
    parser.add_argument("--adam_epsilon", default=1e-8, type=float,
                        help="Epsilon for Adam optimizer.")
    parser.add_argument("--max_grad_norm", default=1.0, type=float,
                        help="Max gradient norm.")
    parser.add_argument("--num_train_epochs", default=3.0, type=float,
                        help="Total number of training epochs to perform.")
    parser.add_argument("--max_steps", default=-1, type=int,
                        help="If > 0: set total number of training steps to perform. Override num_train_epochs.")
    parser.add_argument("--warmup_steps", default=0, type=int,
                        help="Linear warmup over warmup_steps.")
    parser.add_argument("--n_best_size", default=20, type=int,
                        help="The total number of n-best predictions to generate in the nbest_predictions.json output file.")
    parser.add_argument("--max_answer_length", default=30, type=int,
                        help="The maximum length of an answer that can be generated. This is needed because the start "
                             "and end predictions are not conditioned on one another.")
    parser.add_argument("--verbose_logging", action='store_true',
                        help="If true, all of the warnings related to data processing will be printed. "
                             "A number of warnings are expected for a normal SQuAD evaluation.")

    parser.add_argument('--logging_steps', type=int, default=50,
                        help="Log every X updates steps.")
    parser.add_argument('--save_steps', type=int, default=50,
                        help="Save checkpoint every X updates steps.")
    parser.add_argument("--eval_all_checkpoints", action='store_true',
                        help="Evaluate all checkpoints starting with the same prefix as model_name ending and ending with step number")
    parser.add_argument("--no_cuda", action='store_true',
                        help="Whether not to use CUDA when available")
    parser.add_argument('--overwrite_output_dir', action='store_true',
                        help="Overwrite the content of the output directory")
    parser.add_argument('--overwrite_cache', action='store_true',
                        help="Overwrite the cached training and evaluation sets")
    parser.add_argument('--seed', type=int, default=42,
                        help="random seed for initialization")

    parser.add_argument("--local_rank", type=int, default=-1,
                        help="local_rank for distributed training on gpus")
    parser.add_argument('--fp16', action='store_true',
                        help="Whether to use 16-bit (mixed) precision (through NVIDIA apex) instead of 32-bit")
    parser.add_argument('--fp16_opt_level', type=str, default='O1',
                        help="For fp16: Apex AMP optimization level selected in ['O0', 'O1', 'O2', and 'O3']."
                             "See details at https://nvidia.github.io/apex/amp.html")
    parser.add_argument('--server_ip', type=str, default='', help="Can be used for distant debugging.")
    parser.add_argument('--server_port', type=str, default='', help="Can be used for distant debugging.")
    parser.add_argument("--do_calibration", action='store_true',
                        help="Whether to do calibration.")
    parser.add_argument("--do_int8_inference", action='store_true',
                        help="Whether to run int8 inference.")
    parser.add_argument("--do_fp32_inference", action='store_true',
                        help="Whether to run fp32 inference.")
    parser.add_argument("--mkldnn_eval", action='store_true',
                        help="evaluation with MKLDNN")
    parser.add_argument("--tune", action='store_true',
                        help="run Low Precision Optimization Tool to tune int8 acc.")
    parser.add_argument("--task_name", default=None, type=str, required=True,
                        help="SQuAD task")
    parser.add_argument("--warmup", type=int, default=5,
                        help="warmup for performance")
    parser.add_argument('-i', "--iter", default=0, type=int,
                        help='For accuracy measurement only.')
    parser.add_argument('--config', type=str, default='conf.yaml', help="yaml config file")
    parser.add_argument('--benchmark', dest='benchmark', action='store_true',
                        help='run benchmark')
    parser.add_argument('-r', "--accuracy_only", dest='accuracy_only', action='store_true',
                        help='For accuracy measurement only.')
    parser.add_argument("--tuned_checkpoint", default='./saved_results', type=str, metavar='PATH',
                        help='path to checkpoint tuned by Low Precision Optimization Tool (default: ./)')
    parser.add_argument('--int8', dest='int8', action='store_true',
                        help='run benchmark')


    args = parser.parse_args()

    args.predict_file = os.path.join(args.output_dir, 'predictions_{}_{}.txt'.format(
        list(filter(None, args.model_name_or_path.split('/'))).pop(),
        str(args.max_seq_length))
    )

    if os.path.exists(args.output_dir) and os.listdir(args.output_dir) and args.do_train and not args.overwrite_output_dir:
        raise ValueError("Output directory ({}) already exists and is not empty. Use --overwrite_output_dir to overcome.".format(args.output_dir))

    mix_qkv = False
    if args.do_calibration or args.do_int8_inference or args.tune:
       mix_qkv = True

    # Setup distant debugging if needed
    if args.server_ip and args.server_port:
        # Distant debugging - see https://code.visualstudio.com/docs/python/debugging#_attach-to-a-local-script
        import ptvsd
        print("Waiting for debugger attach")
        ptvsd.enable_attach(address=(args.server_ip, args.server_port), redirect_output=True)
        ptvsd.wait_for_attach()

    # Setup CUDA, GPU & distributed training
    if args.local_rank == -1 or args.no_cuda:
        device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
        args.n_gpu = torch.cuda.device_count()
    else:  # Initializes the distributed backend which will take care of sychronizing nodes/GPUs
        torch.cuda.set_device(args.local_rank)
        device = torch.device("cuda", args.local_rank)
        torch.distributed.init_process_group(backend='nccl')
        args.n_gpu = 1
    args.device = device

    # Setup logging
    logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt = '%m/%d/%Y %H:%M:%S',
                        level = logging.INFO if args.local_rank in [-1, 0] else logging.WARN)
    logger.warning("Process rank: %s, device: %s, n_gpu: %s, distributed training: %s, 16-bits training: %s",
                    args.local_rank, device, args.n_gpu, bool(args.local_rank != -1), args.fp16)

    # Set seed
    set_seed(args)

    # Load pretrained model and tokenizer
    if args.local_rank not in [-1, 0]:
        torch.distributed.barrier()  # Make sure only the first process in distributed training will download model & vocab

    args.model_type = args.model_type.lower()
    config_class, model_class, tokenizer_class = MODEL_CLASSES[args.model_type]
    config = config_class.from_pretrained(args.config_name if args.config_name else args.model_name_or_path,
                                          cache_dir=args.cache_dir if args.cache_dir else None)
    tokenizer = tokenizer_class.from_pretrained(args.tokenizer_name if args.tokenizer_name else args.model_name_or_path,
                                                do_lower_case=args.do_lower_case,
                                                cache_dir=args.cache_dir if args.cache_dir else None)
    model = model_class.from_pretrained(args.model_name_or_path,
                                        from_tf=bool('.ckpt' in args.model_name_or_path),
                                        config=config,
                                        mix_qkv=mix_qkv, 
                                        cache_dir=args.cache_dir if args.cache_dir else None)

    if args.local_rank == 0:
        torch.distributed.barrier()  # Make sure only the first process in distributed training will download model & vocab

    model.to(args.device)

    logger.info("Training/evaluation parameters %s", args)

    # Before we do anything with models, we want to ensure that we get fp16 execution of torch.einsum if args.fp16 is set.
    # Otherwise it'll default to "promote" mode, and we'll get fp32 operations. Note that running `--fp16_opt_level="O2"` will
    # remove the need for this code, but it is still valid.
    if args.fp16:
        try:
            import apex
            apex.amp.register_half_function(torch, 'einsum')
        except ImportError:
            raise ImportError("Please install apex from https://www.github.com/nvidia/apex to use fp16 training.")

    # Training
    if args.do_train:
        train_dataset = load_and_cache_examples(args, tokenizer, evaluate=False, output_examples=False)
        global_step, tr_loss = train(args, train_dataset, model, tokenizer)
        logger.info(" global_step = %s, average loss = %s", global_step, tr_loss)


    # Save the trained model and the tokenizer
    if args.do_train and (args.local_rank == -1 or torch.distributed.get_rank() == 0):
        # Create output directory if needed
        if not os.path.exists(args.output_dir) and args.local_rank in [-1, 0]:
            os.makedirs(args.output_dir)

        logger.info("Saving model checkpoint to %s", args.output_dir)
        # Save a trained model, configuration and tokenizer using `save_pretrained()`.
        # They can then be reloaded using `from_pretrained()`
        model_to_save = model.module if hasattr(model, 'module') else model  # Take care of distributed/parallel training
        model_to_save.save_pretrained(args.output_dir)
        tokenizer.save_pretrained(args.output_dir)

        # Good practice: save your training arguments together with the trained model
        torch.save(args, os.path.join(args.output_dir, 'training_args.bin'))

        # Load a trained model and vocabulary that you have fine-tuned
        model = model_class.from_pretrained(args.output_dir, force_download=True, mix_qkv=mix_qkv)
        tokenizer = tokenizer_class.from_pretrained(args.output_dir, do_lower_case=args.do_lower_case)
        model.to(args.device)


    # Evaluation - we can ask to evaluate all the checkpoints (sub-directories) in a directory
    results = {}
    if args.do_eval and args.local_rank in [-1, 0]:
        checkpoints = [args.output_dir]
        if args.eval_all_checkpoints:
            checkpoints = list(os.path.dirname(c) for c in sorted(glob.glob(args.output_dir + '/**/' + WEIGHTS_NAME, recursive=True)))
            logging.getLogger("transformers.modeling_utils").setLevel(logging.WARN)  # Reduce model loading logs

        logger.info("Evaluate the following checkpoints: %s", checkpoints)

        for checkpoint in checkpoints:
            # Reload the model
            global_step = checkpoint.split('-')[-1] if len(checkpoints) > 1 else ""
            if args.mkldnn_eval or args.do_fp32_inference:
               model = model_class.from_pretrained(checkpoint, force_download=True)
               model.to(args.device)

               # Evaluate
               result, _ = evaluate(args, model, tokenizer, prefix=global_step)
               result = dict((k + ('_{}'.format(global_step) if global_step else ''), v) for k, v in result.items())
               results.update(result)

            if args.tune:
                def eval_func_for_lpot(model):
                    result, _ = evaluate(args, model, tokenizer)
                    for key in sorted(result.keys()):
                        logger.info("  %s = %s", key, str(result[key]))
                    bert_task_acc_keys = ['best_f1', 'f1', 'mcc', 'spearmanr', 'acc']
                    for key in bert_task_acc_keys:
                        if key in result.keys():
                            logger.info("Finally Eval {}:{}".format(key, result[key]))
                            acc = result[key]
                            break
                    return acc

                model = model_class.from_pretrained(checkpoint, force_download=True, mix_qkv=True)
                model.to(args.device)
                dataset = load_and_cache_examples(args, tokenizer, evaluate=True, output_examples=False)
                args.eval_batch_size = args.per_gpu_eval_batch_size * max(1, args.n_gpu)
                eval_task = "squad"
                from lpot import Quantization
                quantizer = Quantization(args.config)
                dataset = quantizer.dataset('bert', dataset=dataset, task=eval_task,
                                            model_type=args.model_type)
                test_dataloader = quantizer.dataloader(dataset, batch_size=args.eval_batch_size)
                q_model = quantizer(model, test_dataloader, eval_func=eval_func_for_lpot)
                q_model.save(args.tuned_checkpoint)
                exit(0)

            if args.benchmark or args.accuracy_only:
                model = model_class.from_pretrained(checkpoint, mix_qkv=True)
                model.to(args.device)
                if args.int8:
                    from lpot.utils.pytorch import load
                    new_model = load(
                        os.path.abspath(os.path.expanduser(args.tuned_checkpoint)), model)
                else:
                    new_model = model
                result, _ = evaluate(args, new_model, tokenizer, prefix=global_step)
                exit(0)

            if args.do_calibration:
               model = model_class.from_pretrained(checkpoint, force_download=True, mix_qkv=True)
               model.to(args.device)
               model.qconfig = default_per_channel_qconfig
               propagate_qconfig_(model)
               add_observer_(model)
               # Evaluate
               evaluate(args, model, tokenizer, prefix=global_step, calibration=True)
               convert(model, inplace = True)
               quantized_model_path = "squad" + str(global_step) + "_quantized_model" 
               if not os.path.exists(quantized_model_path):
                        os.makedirs(quantized_model_path)
               model.save_pretrained(quantized_model_path)
               result, _ = evaluate(args, model, tokenizer, prefix=global_step)
               result = dict((k + ('_{}'.format(global_step) if global_step else ''), v) for k, v in result.items())
               results.update(result)
            if args.do_int8_inference:
               model = model_class.from_pretrained(checkpoint, force_download=True, mix_qkv=True)
               model.to(args.device)
               model.qconfig = default_per_channel_qconfig
               propagate_qconfig_(model)
               add_observer_(model)
               convert(model, inplace = True)
               quantized_model_path = "squad" + str(global_step) + "_quantized_model"
               if not os.path.exists(quantized_model_path):
                        logger.info("Please run calibration first!")
                        return 
               model_bin_file = os.path.join(quantized_model_path,"pytorch_model.bin" )
               state_dict = torch.load(model_bin_file)
               model.load_state_dict(state_dict)
               print(model)
               with torch.autograd.profiler.profile() as prof:
                    result, _ = evaluate(args, model, tokenizer, prefix=global_step)
               print(prof.key_averages().table(sort_by="cpu_time_total"))
               result = dict((k + ('_{}'.format(global_step) if global_step else ''), v) for k, v in result.items())
               results.update(result)
    logger.info("Results: {}".format(results))

    return results


if __name__ == "__main__":
    main()
