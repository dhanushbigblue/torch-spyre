# Copyright 2026 The Torch-Spyre Authors.
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

"""tests/oot_framework/utils/filter_configs.py: label selection logic."""

import importlib.util
from pathlib import Path

import yaml

HELPER = (
    Path(__file__).resolve().parent / "oot_framework" / "utils" / "filter_configs.py"
)
_spec = importlib.util.spec_from_file_location("filter_configs", HELPER)
assert _spec is not None and _spec.loader is not None
filter_configs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(filter_configs)


def _write_config(tmp_path, *, labels=None):
    cfg = {"test_suite_config": {}}
    if labels is not None:
        cfg["test_suite_config"]["labels"] = labels
    path = tmp_path / "config.yaml"
    path.write_text(yaml.dump(cfg))
    return path


def test_load_labels(tmp_path):
    path = _write_config(tmp_path, labels=["trunk"])
    assert filter_configs._load_labels(path) == ["trunk"]


def test_load_labels_absent(tmp_path):
    path = _write_config(tmp_path)
    assert filter_configs._load_labels(path) == []
