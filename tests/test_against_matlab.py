"""Regression tests against reference .mat files in benchmark/."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from compare_matlab import (
    BENCHMARK_DIR,
    INPUT_FILES_DIR,
    REPO_ROOT,
    compare_arrays,
    load_mat,
    mat_struct_field,
    max_abs_diff,
)

DEMO_JSON = "Demo_WavelengthMode_CF_sphere.json"


@pytest.fixture(scope="module")
def read_settings_py():
    sys.path.insert(0, str(REPO_ROOT / "Functions"))
    from ReadSettings_v1 import ReadSettings

    return ReadSettings(str(INPUT_FILES_DIR / DEMO_JSON))


@pytest.fixture(scope="module")
def read_settings_mat():
    return load_mat(BENCHMARK_DIR / "ReadSettings.mat")


def test_readsettings_k0_matches_matlab(read_settings_py, read_settings_mat):
    k0_py = np.asarray(read_settings_py["Settings"]["k0"]).ravel()
    k0_mat = np.asarray(mat_struct_field(read_settings_mat["Settings"], "k0")).ravel()
    compare_arrays(k0_py, k0_mat, name="k0")


def test_readsettings_nr_matches_matlab(read_settings_py, read_settings_mat):
    nr_py = np.asarray(read_settings_py["Settings"]["nr"])
    nr_mat = np.asarray(mat_struct_field(read_settings_mat["Settings"], "nr"))
    compare_arrays(nr_py, nr_mat, name="nr", rtol=1e-14, atol=1e-14)


def test_readsettings_lambda_matches_matlab(read_settings_py, read_settings_mat):
    lam_py = np.asarray(read_settings_py["Settings"]["lambda"]).ravel()
    lam_mat = np.asarray(mat_struct_field(read_settings_mat["Settings"], "lambda")).ravel()
    compare_arrays(lam_py, lam_mat, name="lambda")


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
