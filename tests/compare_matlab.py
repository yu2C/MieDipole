"""Utilities for comparing Python output against reference .mat files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import scipy.io as sio

REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_DIR = REPO_ROOT / "benchmark"
FUNCTIONS_DIR = REPO_ROOT / "Functions"
INPUT_FILES_DIR = REPO_ROOT / "InputFiles"


def load_mat(path: Path | str) -> dict[str, Any]:
    data = sio.loadmat(path, squeeze_me=True, struct_as_record=False)
    return {k: v for k, v in data.items() if not k.startswith("__")}


def mat_struct_field(struct_array: Any, name: str) -> Any:
    """Extract a field from a MATLAB struct loaded by scipy."""
    if hasattr(struct_array, name):
        return getattr(struct_array, name)
    if isinstance(struct_array, np.ndarray) and struct_array.dtype.names:
        return struct_array[name]
    item = struct_array[0, 0] if isinstance(struct_array, np.ndarray) and struct_array.ndim >= 2 else struct_array
    if hasattr(item, name):
        return getattr(item, name)
    return item[name]


def compare_arrays(
    actual: np.ndarray,
    expected: np.ndarray,
    *,
    name: str = "array",
    rtol: float = 1e-10,
    atol: float = 1e-12,
) -> None:
    actual = np.asarray(actual)
    expected = np.asarray(expected)
    if actual.shape != expected.shape:
        raise AssertionError(f"{name}: shape {actual.shape} != {expected.shape}")

    if np.issubdtype(actual.dtype, np.complexfloating) or np.issubdtype(
        expected.dtype, np.complexfloating
    ):
        diff = np.max(np.abs(actual - expected))
        scale = max(np.max(np.abs(expected)), 1e-30)
        if diff > atol + rtol * scale:
            raise AssertionError(
                f"{name}: max abs diff {diff:.3e} (tol {atol + rtol * scale:.3e})"
            )
        return

    np.testing.assert_allclose(actual, expected, rtol=rtol, atol=atol, err_msg=name)


def max_abs_diff(actual: np.ndarray, expected: np.ndarray) -> float:
    return float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
