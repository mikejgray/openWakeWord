# Copyright 2022 David Scripka. All rights reserved.
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
# Copyright 2022 David Scripka. All rights reserved.
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


# Imports
import openwakeword
import os
from pathlib import Path
import collections

# Models and corresponding files

test_dict = {
    "hey_mycroft_v1": ["hey_mycroft_v1_test.wav"],
    "alexa_v5": ["alexa_v5_test.wav"]
}


# Tests
class TestModels:
    def test_models(self):
        models = [str(i) for i in Path(
                    os.path.join("openwakeword", "resources", "models")
                  ).glob("**/*.onnx")
                  if "embedding" not in str(i) and "melspec" not in str(i)]
        owwModel = openwakeword.Model(
            wakeword_model_paths=models,
        )

        for model, clips in test_dict.items():
            for clip in clips:
                # Get predictions for reach frame in the clip
                predictions = owwModel.predict_clip(os.path.join("tests", "data", clip))

                # Make predictions dictionary flatter
                predictions_flat = collections.defaultdict(list)
                [predictions_flat[key].append(i[key]) for i in predictions for key in i.keys()]

            # Check scores against default threshold (0.5), skipping first prediction as it is innaccurate
            for key in predictions_flat.keys():
                if key in clip:
                    assert max(predictions_flat[key][1:]) >= 0.5
                else:
                    assert max(predictions_flat[key][1:]) < 0.5
