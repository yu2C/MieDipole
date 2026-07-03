# MieDipole — Python Version

Python port of [MieDipole](https://github.com/yu2C/MieDipole) (MATLAB original on `main` branch).

This code lives on the **`yu-py`** branch of the public MieDipole repository.

## Requirements

- Python >= 3.9, < 3.13
- [uv](https://docs.astral.sh/uv/) (recommended)

## Setup (uv — isolated environment)

```bash
uv sync          # creates .venv/ and installs pinned deps from uv.lock
```

## Run

```bash
cd 123/function
uv run --project ../.. python main.py
```

Default input: `Demo_WavelengthMode_CF_sphere.json` (in the same directory).

## Directory Layout

```
MieDipole/  (yu-py branch)
├── pyproject.toml, uv.lock, requirements.txt
├── 123/
│   ├── function/          ← runtime: main.py + all Python modules + demo inputs
│   └── InputFiles/        ← reference JSON/CSV (mirror of main branch)
├── benchmark/             ← .mat validation data (MATLAB ↔ Python comparison)
└── archive/
    ├── scratch/           ← temporary scratch files
    ├── notes/             ← development notes
    └── dev/               ← non-runtime development history (not used by main.py)
        ├── function_early/
        ├── SphBessel/, NormTauPiP/, vecTran/
        ├── Functions/     ← MATLAB reference copies
        └── Tutorial/
```

| Path | Description |
|------|-------------|
| `123/function/` | **Entry point** — do not move without updating imports |
| `123/InputFiles/` | Input JSON/CSV compatible with MATLAB `main` branch |
| `benchmark/` | Saved `.mat` outputs for cross-validation |
| `archive/dev/` | Historical development files, preserved but not used at runtime |

## Relation to MATLAB Version

| Branch | Language | Status |
|--------|----------|--------|
| `main` | MATLAB | Stable, reference |
| `yu-py` | Python | Work in progress — validate against `main` |

Input JSON format is compatible with the MATLAB version's `InputFiles/`.

## Citation

Same as the MATLAB version — see the main [README](https://github.com/yu2C/MieDipole/blob/main/README.md#Citation).
