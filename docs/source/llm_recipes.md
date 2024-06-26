## LLMs Quantization Recipes

Intel® Neural Compressor supported advanced large language models (LLMs) quantization technologies including SmoothQuant (SQ) and Weight-Only Quant (WOQ),
and verified a list of LLMs on 4th Gen Intel® Xeon® Scalable Processor (codenamed Sapphire Rapids) with [PyTorch](https://pytorch.org/),
[Intel® Extension for PyTorch](https://github.com/intel/intel-extension-for-pytorch) and [Intel® Extension for Transformers](https://github.com/intel/intel-extension-for-transformers).  
This document aims to publish the specific recipes we achieved for the popular LLMs and help users to quickly get an optimized LLM with limited 1% accuracy loss.

> Notes:
>
> - The quantization algorithms provide by [Intel® Neural Compressor](https://github.com/intel/neural-compressor) and the evaluate functions provide by [Intel® Extension for Transformers](https://github.com/intel/intel-extension-for-transformers).
> - The model list are continuing update, please expect to find more LLMs in the future.

## IPEX key models

|             Models              | SQ INT8 | WOQ INT8 | WOQ INT4 |
| :-----------------------------: | :-----: | :------: | :------: |
|       EleutherAI/gpt-j-6b       |    ✔    |    ✔     |    ✔     |
|        facebook/opt-1.3b        |    ✔    |    ✔     |    ✔     |
|        facebook/opt-30b         |    ✔    |    ✔     |    ✔     |
|    meta-llama/Llama-2-7b-hf     |    ✔    |    ✔     |    ✔     |
|    meta-llama/Llama-2-13b-hf    |    ✔    |    ✔     |    ✔     |
|    meta-llama/Llama-2-70b-hf    |    ✔    |    ✔     |    ✔     |
|        tiiuae/falcon-7b         |    ✔    |    ✔     |    ✔     |
|        tiiuae/falcon-40b        |    ✔    |    ✔     |    ✔     |
| baichuan-inc/Baichuan-13B-Chat  |    ✔    |    ✔     |    ✔     |
| baichuan-inc/Baichuan2-13B-Chat |    ✔    |    ✔     |    ✔     |
| baichuan-inc/Baichuan2-7B-Chat  |    ✔    |    ✔     |    ✔     |
|      bigscience/bloom-1b7       |    ✔    |    ✔     |    ✔     |
|     databricks/dolly-v2-12b     |    ✖    |    ✔     |    ✖     |
|     EleutherAI/gpt-neox-20b     |    ✖    |    ✔     |    ✔     |
|    mistralai/Mistral-7B-v0.1    |    ✖    |    ✔     |    ✔     |
|        THUDM/chatglm2-6b        |   WIP   |    ✔     |    ✔     |
|        THUDM/chatglm3-6b        |   WIP   |    ✔     |    ✔     |

**Detail recipes can be found [HERE](https://github.com/intel/intel-extension-for-transformers/blob/main/examples/huggingface/pytorch/text-generation/quantization/llm_quantization_recipes.md).**

> Notes:
>
> - This model list comes from [IPEX](https://intel.github.io/intel-extension-for-pytorch/cpu/latest/tutorials/llm.html).
> - The WIP recipes will be published soon.
