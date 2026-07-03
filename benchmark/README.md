# Benchmark Data

Reference `.mat` files used for **regression testing** during the MATLAB → Python port.

## Regression reference (active)

| File | Purpose |
|------|---------|
| `regression/CF_sphere_py.mat` | End-to-end CF output for `Demo_WavelengthMode_CF_sphere.json` |
| `ReadSettings.mat` | ReadSettings intermediate values (from original MATLAB run) |

## Historical / module-level

Intermediate results (`TwoGR0_*.mat`, `SourCoeff_*.mat`, `VectSphFunc.mat`, …) were saved during porting for module-by-module debugging. Useful for future test expansion.

Files with `_py` suffix in variable names are Python snapshots from development.

## Refresh regression baseline

Refresh regression baseline:

```bash
uv run python main.py
cp main_result.mat benchmark/regression/CF_sphere_py.mat
uv run pytest tests/ -v
```
