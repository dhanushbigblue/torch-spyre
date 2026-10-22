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

"""oot_checker.checks.check_invalid_exclude_plat_tags: typo'd exclude__plat_* tags."""

from pathlib import Path

import pytest
from oot_checker.checks import KNOWN_PLATFORMS, check_invalid_exclude_plat_tags


@pytest.mark.parametrize(
    "tags,expected",
    [
        (["exclude__plat_ppc64le"], 0),  # known suffix
        ([], 0),  # no tags at all
        (["exclude__plat_PPC64LE"], 0),  # known suffix, mixed case
        (["exclude__plat_ppc64"], 1),  # typo: missing 'le'
        (["exclude__plat_power"], 1),  # typo: wrong name
        (["model__Qwen2.5-7B-Instruct"], 0),  # non-exclude tag, ignored
        (["model__Qwen2.5-7B-Instruct", "exclude__plat_ppc64le"], 0),  # mixed, valid
        (["model__Qwen2.5-7B-Instruct", "exclude__plat_ppc64"], 1),  # mixed, typo
    ],
)
def test_check_invalid_exclude_plat_tags(tags, expected):
    assert check_invalid_exclude_plat_tags({Path("a.yaml"): tags}) == expected


def test_known_platforms_contains_expected_values():
    # Pinned exactly: a silent edit here (e.g. dropping "s390x") would make
    # check_invalid_exclude_plat_tags stop flagging a real typo for that arch,
    # and the parametrized cases above wouldn't catch it since none exercise it.
    assert KNOWN_PLATFORMS == {"x86_64", "ppc64le", "s390x", "aarch64"}
