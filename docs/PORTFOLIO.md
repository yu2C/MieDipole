# Portfolio Notes

See [README.md](README.md) for setup and usage.

This document is for resume / interview preparation.

## One-liner (English)

> Python port of Generalized Mie Theory for plasmonic resonance energy transfer — computes dipole coupling factors for spherical nanostructures using vector spherical harmonic expansion.

## One-liner (中文)

> 以 Python 重現廣義 Mie 散射理論，計算電偶極源激發下球形 / 核殼奈米結構的電磁耦合因子（Coupling Factor），應用於表面 plasmon 共振能量轉移研究。

## Resume bullets (English)

- Ported a published MATLAB computational physics codebase (~40 modules) to Python using NumPy/SciPy, preserving numerical agreement with reference data
- Implemented complex dielectric interpolation, vector spherical harmonics, and Mie expansion for wavelength / angle / mapping scan modes
- Set up reproducible dev environment with `uv`, pinned dependencies, and pytest regression tests
- Organized open-source repository with clear structure, documentation, and CI-ready test suite on GitHub (`yu-py` branch)

## Resume bullets (中文)

- 將已發表之 MATLAB 計算物理程式（約 40 個模組）移植為 Python（NumPy / SciPy），並以 regression test 確保數值結果一致
- 實作複數介電函數插值、向量球諧函數展開與 Mie 散射計算，支援波長 / 角度 / 平面 mapping 等多種模式
- 使用 uv 建立可重現開發環境，撰寫 pytest 測試與專案文件，公開於 GitHub

## Talking points (interview)

1. **Why port?** MATLAB license barrier → open Python stack for reproducibility and sharing
2. **Hardest bug:** `PchipInterpolator` does not accept complex arrays — split real/imag interpolation to match MATLAB `interp1(..., 'pchip')`
3. **Validation without MATLAB:** module-level `.mat` checkpoints + end-to-end regression baseline
4. **Physics context:** Coupling Factor from JPCL 2020 — plasmon-enhanced resonance energy transfer

## Links

- Repo: https://github.com/yu2C/MieDipole/tree/yu-py
- Paper: https://pubs.acs.org/doi/10.1021/acs.jpclett.0c01989
