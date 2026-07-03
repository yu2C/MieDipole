"""Generate example figure for README from main_result.mat."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import scipy.io as sio  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"


def main() -> None:
    sys.path.insert(0, str(ROOT / "Functions"))
    from ReadSettings_v1 import ReadSettings

    settings = ReadSettings(str(ROOT / "InputFiles" / "Demo_WavelengthMode_CF_sphere.json"))["Settings"]
    result = sio.loadmat(ROOT / "main_result.mat")

    lambda_val = np.asarray(settings["lambda"]).ravel()
    x = 1.0 / lambda_val * 1e-2
    cf = result["CF_py"].ravel()
    cfdip = result["CFdip_py"].ravel()

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.semilogy(x, cf, "k-", label="CF (sphere)")
    ax.semilogy(x, cfdip, "r--", label="CF (vacuum)")
    ax.set_xlabel(r"Wavenumber (cm$^{-1}$)")
    ax.set_ylabel(r"Coupling Factor (cm$^{-6}$)")
    ax.set_title("Demo: WavelengthMode CF — Ag sphere")
    ax.legend()
    fig.tight_layout()

    DOCS_DIR.mkdir(exist_ok=True)
    out = DOCS_DIR / "example_cf_sphere.png"
    fig.savefig(out, dpi=150)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
