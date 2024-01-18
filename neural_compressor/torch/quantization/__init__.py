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

from .config import (
    get_default_rtn_config,
    get_default_gptq_config,
    RTNConfig,
    GPTQConfig,
)
from .quantize import quantize, quantize_dynamic

# TODO(Yi): move config to config.py
from .autotune import autotune, TuningConfig, get_default_tune_config

### Quantization Function Registration ###
import neural_compressor.torch.quantization.weight_only
from neural_compressor.torch.utils import is_hpex_available

if is_hpex_available():
    import neural_compressor.torch.quantization.fp8
