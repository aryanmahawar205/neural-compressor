# -*- coding: utf-8 -*-
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
"""Test ModelRepository."""

import unittest

from neural_insights.components.model.repository import ModelRepository
from neural_insights.utils.consts import Frameworks
from neural_insights.utils.exceptions import NotFoundException


class TestModelRepository(unittest.TestCase):
    """Test ModelRepository class."""

    def test_onnx_is_model_path(self) -> None:
        """Test if onnx file is recognized correctly."""
        path = "/home/user/model.onnx"
        result = ModelRepository.is_model_path(path)
        self.assertTrue(result)

    def test_mp3_is_model_path(self) -> None:
        """Test if mp3 file is recognized correctly."""
        path = "/home/user/favourite_song.mp3"
        result = ModelRepository.is_model_path(path)
        self.assertFalse(result)

    def test_get_frameworks(self) -> None:
        """Test getting frameworks."""
        expected = [Frameworks.ONNX.value, Frameworks.PT.value, Frameworks.TF.value]

        repository = ModelRepository()
        actual = repository.get_frameworks()

        self.assertEqual(expected, actual)

    def test_framework_from_path_for_known_model(self) -> None:
        """Test get_framework_from_path."""
        actual = ModelRepository.get_framework_from_path("/home/user/model.onnx")
        self.assertEqual(Frameworks.ONNX.value, actual)

    def test_framework_from_path_for_unknown_model(self) -> None:
        """Test get_framework_from_path."""
        with self.assertRaises(NotFoundException):
            ModelRepository.get_framework_from_path("/home/user/favourite_song.mp3")


if __name__ == "__main__":
    unittest.main()
