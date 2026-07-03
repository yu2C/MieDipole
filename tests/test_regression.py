"""Regression tests for the Python port."""

from __future__ import annotations

import subprocess
import sys

import numpy as np
import pytest

from compare_matlab import BENCHMARK_DIR, REPO_ROOT, compare_arrays, load_mat, max_abs_diff


@pytest.fixture(scope="module")
def main_result_py():
    subprocess.run(
        [sys.executable, "main.py"],
        cwd=REPO_ROOT,
        env={**dict(__import__("os").environ), "MPLBACKEND": "Agg"},
        check=True,
    )
    return load_mat(REPO_ROOT / "main_result.mat")


def test_main_cf_self_consistent(main_result_py):
    first = {k: np.array(v) for k, v in main_result_py.items()}
    subprocess.run(
        [sys.executable, "main.py"],
        cwd=REPO_ROOT,
        env={**dict(__import__("os").environ), "MPLBACKEND": "Agg"},
        check=True,
    )
    second = load_mat(REPO_ROOT / "main_result.mat")
    for key in ("CF_py", "CFdip_py", "EF_py"):
        assert max_abs_diff(first[key], second[key]) == 0.0, key


def test_main_cf_matches_regression_baseline(main_result_py):
    golden = load_mat(BENCHMARK_DIR / "regression" / "CF_sphere_py.mat")
    for key in ("CF_py", "CFdip_py", "EF_py"):
        compare_arrays(main_result_py[key], golden[key], name=key)
