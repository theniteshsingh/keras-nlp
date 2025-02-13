# Copyright 2023 The KerasNLP Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from keras_nlp.models.distil_bert.distil_bert_tokenizer import (
    DistilBertTokenizer,
)
from keras_nlp.tests.test_case import TestCase


class DistilBertTokenizerTest(TestCase):
    def setUp(self):
        self.vocab = ["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"]
        self.vocab += ["THE", "QUICK", "BROWN", "FOX"]
        self.vocab += ["the", "quick", "brown", "fox"]
        self.init_kwargs = {"vocabulary": self.vocab}
        self.input_data = ["THE QUICK BROWN FOX", "THE FOX"]

    def test_tokenizer_basics(self):
        self.run_preprocessing_layer_test(
            cls=DistilBertTokenizer,
            init_kwargs=self.init_kwargs,
            input_data=self.input_data,
            expected_output=[[5, 6, 7, 8], [5, 8]],
        )

    def test_lowercase(self):
        tokenizer = DistilBertTokenizer(vocabulary=self.vocab, lowercase=True)
        output = tokenizer(self.input_data)
        self.assertAllEqual(output, [[9, 10, 11, 12], [9, 12]])

    def test_errors_missing_special_tokens(self):
        with self.assertRaises(ValueError):
            DistilBertTokenizer(vocabulary=["a", "b", "c"])

    @pytest.mark.large
    def test_smallest_preset(self):
        self.run_preset_test(
            cls=DistilBertTokenizer,
            preset="distil_bert_base_en_uncased",
            input_data=["The quick brown fox."],
            expected_output=[[1996, 4248, 2829, 4419, 1012]],
        )

    @pytest.mark.extra_large
    def test_all_presets(self):
        for preset in DistilBertTokenizer.presets:
            self.run_preset_test(
                cls=DistilBertTokenizer,
                preset=preset,
                input_data=self.input_data,
            )
