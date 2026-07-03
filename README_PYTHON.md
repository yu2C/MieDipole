# MieDipole — Python Version

Python port of [MieDipole](https://github.com/yu2C/MieDipole) (MATLAB original on `main` branch).

This code lives on the **`yu-py`** branch of the public MieDipole repository.

## Requirements

- Python >= 3.9
- See `requirements.txt` (pinned) or `pyproject.toml` (uv-ready)

### Install (pip)

```bash
pip install -r requirements.txt
```

### Install (uv)

```bash
uv sync
```

## Entry Point

The main program is located at:

```
123/function/main.py
```

Run from the `123/function/` directory:

```bash
cd 123/function
python main.py
```

Default input: `Demo_WavelengthMode_CF_sphere.json` (place JSON files in the working directory or adjust `FilePath` / `FileName` in `main.py`).

## Directory Layout

| Path | Description |
|------|-------------|
| `123/function/` | **Main Python modules** — entry point and core functions |
| `123/InputFiles/` | JSON input files for calculations |
| `123/SphBessel/` | Spherical Bessel function development & tests |
| `123/NormTauPiP/` | Normalized tau/pi function development & tests |
| `123/vecTran/` | Vector translation (Wigner-d) development & tests |
| `function/` | Early Python port attempts (superseded by `123/function/`) |
| `*.mat` (root) | MATLAB benchmark data for validation |

## Relation to MATLAB Version

| Branch | Language | Status |
|--------|----------|--------|
| `main` | MATLAB | Stable, original |
| `yu-py` | Python | Work in progress |

Input JSON format is compatible with the MATLAB version's `InputFiles/`.

## Citation

Same as the MATLAB version — see the main [README](https://github.com/yu2C/MieDipole/blob/main/README.md#Citation).
