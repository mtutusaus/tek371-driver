# Tektronix TEK371 high power curve tracer controller

> **Note:** This project is heavily based on code originally written by **[David](https://github.com/sansanda/pymeasure/blob/dev/tek371A/pymeasure/instruments/tektronix/tek371A.py)**.

This repository has all the commands and functions necessary to control the Tektronix TEK371 high power curve tracer using PyVISA. Its intended use is to perform I-V curves of power semiconductor devices, even though the equipment is capable of much more. The functions to control other aspects rather than the I-V curves are implemented, but not tested.

---

## Features
- Control Tektronix TEK371 via GPIB using PyVISA.
- Perform automated I-V curve measurements for power semiconductors.
  
---

## Requirements
- Python 3.10 (not tested with other versions)
- [PyVISA](https://pyvisa.readthedocs.io/)
- GPIB interface (e.g., NI GPIB-USB adapter)

---

## Usage
See [test](tests/test_instrument.py) for a script to perform any number of consecutive I-V measurements of a power diode.

---
## **License**
This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit
- **NonCommercial** — You may not use the material for commercial purposes
- **ShareAlike** — Derivatives must use the same license

See the [LICENSE](LICENSE) file for the full license text.

## Acknowledgments

- I would like to acknowledge **[David](https://github.com/sansanda/pymeasure/blob/dev/tek371A/pymeasure/instruments/tektronix/tek371A.py)** for the original implementation that served as the foundation for this project.
- M365 Copilot (Microsoft) for development assistance

## Author

[Miquel Tutusaus](https://github.com/mtutusaus), 2025
