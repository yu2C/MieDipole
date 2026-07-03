# MieDipole (Python)

Python implementation of **Generalized Mie Theory** for a spherical scatterer illuminated by an electric dipole source.

Ported from the MATLAB codebase on the [`main`](https://github.com/yu2C/MieDipole/tree/main) branch. This branch (`yu-py`) is the actively maintained Python version.

**Reference paper:** Lee & Hsu, *J. Phys. Chem. Lett.* **2020**, *11*, 6796–6804. [DOI: 10.1021/acs.jpclett.0c01989](https://pubs.acs.org/doi/10.1021/acs.jpclett.0c01989)

## Highlights

- Computes **coupling factor (CF)**, Purcell factor, and related electromagnetic quantities for sphere / core-shell geometries
- Supports **wavelength**, **angle**, and **mapping** calculation modes via JSON input files
- Vector spherical harmonic expansion (Mie + dipole source formalism)
- Validated with regression tests against saved reference data

## Tech Stack

Python 3.10 · NumPy · SciPy · Matplotlib · pandas · [uv](https://docs.astral.sh/uv/)

## Quick Start

```bash
git clone -b yu-py https://github.com/yu2C/MieDipole.git
cd MieDipole
uv sync

cd 123/function
uv run --project ../.. python main.py
```

Default demo: `Demo_WavelengthMode_CF_sphere.json` (Ag nanosphere, CF vs wavelength).

![Example output](docs/example_cf_sphere.png)

## Project Structure

```
├── 123/function/       Main program (main.py) and core modules
├── 123/InputFiles/     JSON / CSV input templates
├── benchmark/          Reference .mat data for regression tests
├── tests/              pytest suite
├── docs/               Example output figures
└── archive/dev/        Development history (not used at runtime)
```

## Tests

```bash
uv run pytest tests/ -v
```

## Branches

| Branch | Language | Description |
|--------|----------|-------------|
| `main` | MATLAB | Original reference implementation |
| `yu-py` | Python | Python port (this branch) |

## Input Format

JSON files follow the same schema as the MATLAB version. See [`123/InputFiles/`](123/InputFiles/) for examples.

Key fields: geometry (`BC`, `rbc`, dipole positions), dielectric functions (`epsi0`, `epsi1`, …), wavelength range (`lambda_s`, `lambda_e`), and output quantity (`CF`, `Purcell`, …).

## Citation

```bibtex
@article{Lee2020,
    author  = {Lee, Ming-Wei and Hsu, Liang-Yan},
    title   = {Controllable Frequency Dependence of Resonance Energy Transfer Coupled with Localized Surface Plasmon Polaritons},
    journal = {J. Phys. Chem. Lett.},
    volume  = {11},
    number  = {16},
    pages   = {6796--6804},
    year    = {2020},
    doi     = {10.1021/acs.jpclett.0c01989}
}
```

## License

Same as the upstream [MieDipole](https://github.com/yu2C/MieDipole) repository.
