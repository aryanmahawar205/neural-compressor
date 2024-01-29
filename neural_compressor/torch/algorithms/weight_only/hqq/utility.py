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

import inspect
import time

import numpy as np
import torch


def custom_print(message):
    return
    # Get the caller's frame information
    frame = inspect.currentframe()
    caller_frame = inspect.getouterframes(frame)[1]

    # Extract function name from the frame
    func_name = caller_frame[3]

    print(f"[custom_print - {func_name}]: {message}")


def compare_two_tensor(a, b, rtol=1e-05, msg=""):
    #
    print(f"[compare_two_tensor] {msg}")
    assert a.shape == b.shape, "The shape of the two tensor is not the same, got a: {} and b: {}".format(
        a.shape, b.shape
    )
    assert torch.allclose(a, b, rtol=rtol), "The two tensor is not the same, got a: {} and b: {}".format(a, b)


import gc


def cleanup():
    torch.cuda.empty_cache()
    gc.collect()


def is_divisible(val1, val2):
    return int(val2 * np.ceil(val1 / val2)) == val1


def make_multiple(val, multiple):
    return int(multiple * np.ceil(val / float(multiple)))


# decorator to dump function name and args and args value
def inspect_function(func):
    def wrapper(*args, **kwargs):
        print(f"Function Name: {func.__name__}")
        print("Argument Names and Values:")

        # Print positional arguments and values
        for arg_name, arg_value in zip(func.__code__.co_varnames, args):
            if isinstance(arg_value, torch.Tensor):
                print(f"  {arg_name}: {arg_value.shape}")
            else:
                print(f"  {arg_name}: {arg_value}")

        # Print keyword arguments and values
        for arg_name, arg_value in kwargs.items():
            if isinstance(arg_value, torch.Tensor):
                print(f"  {arg_name}: {arg_value.shape}")
            else:
                print(f"  {arg_name}: {arg_value}")

        # Call the original function
        result = func(*args, **kwargs)

        # Optionally, you can print the result
        # print(f"Result: {result}")

        return result

    return wrapper


def dump_elapsed_time(customized_msg=""):
    """Get the elapsed time for decorated functions.

    Args:
        customized_msg (string, optional): The parameter passed to decorator. Defaults to None.
    """

    def f(func):
        def fi(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            end = time.time()
            print(
                "%s elapsed time: %s ms"
                % (
                    customized_msg if customized_msg else func.__qualname__,
                    round((end - start) * 1000, 2),
                )
            )
            return res

        return fi

    return f
