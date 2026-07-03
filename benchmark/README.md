# Benchmark / Golden Reference Files

These `.mat` files were saved during MATLAB → Python porting.  
**Treat files without `_py` suffix in variable names as MATLAB (`main` branch) golden reference.**

## MATLAB golden (compare Python against these)

| File | Variables | Module |
|------|-----------|--------|
| `ReadSettings.mat` | `Settings`, `error_msg` | ReadSettings |
| `TwoGR0_*.mat` | Layer0, Source, Temp, … | TwoGR0 |
| `SourCoeff_*.mat` | p, q, M, N, … | SourCoeff |
| `VectSphFunc.mat` | `M`, `N` | VectSphFunc |
| `VectSphFunc_Rad.mat` | radial functions | SphBessel |

## Python snapshots (self-benchmark, not MATLAB)

| File | Note |
|------|------|
| `*_pyvalues` in NormTauPiP_*.mat | Python export during dev |
| `ReadSettings_py.mat` | Python ReadSettings snapshot |
| `benchmark_of_*.mat` | Python module output |

## Needs refresh

| File | Note |
|------|------|
| `main_result.mat` | Contains `CF_py` keys; **does not match** current `main.py` output. Re-export from MATLAB `Main.m` when available. |

### How to add MATLAB end-to-end golden

In MATLAB (`main` branch), after running `Demo_WavelengthMode_CF_sphere.json`:

```matlab
save('benchmark/golden/CF_sphere.mat', 'CF', 'CFdip', 'EF', 'NormEtot');
```

Then Python tests can compare against `CF` (no `_py` suffix).
