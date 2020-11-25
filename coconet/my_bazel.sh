# Copyright 2020 The Magenta Authors.
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

#!/bin/bash

set -x
set -e

# Pass path to checkpoint directory as first argument to this script.
# You can also download a model pretrained on the J.S. Bach chorales dataset from here:
# http://download.magenta.tensorflow.org/models/coconet/checkpoint.zip
# and pass the path up to the inner most directory as first argument when running this
# script.
checkpoint=../../../repository/coconet_model

# Change this to path for saving samples.
generation_output_dir=./samples

# Generation parameters.
# Number of samples to generate in a batch.
gen_batch_size=2
piece_length=32
strategy=harmonize_midi_melody
tfsample=true
melody_path=./midis/test.mid

# Run command.
PYTHONIOENCODING=utf-8 python coconet_sample.py \
--checkpoint="$checkpoint" \
--gen_batch_size=$gen_batch_size \
--temperature=0.99 \
--strategy=$strategy \
--tfsample=$tfsample \
--generation_output_dir=$generation_output_dir \
--logtostderr \
--prime_midi_melody_fpath="$melody_path"
