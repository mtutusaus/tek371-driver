# Tektronix TEK371 high power curve tracer controller

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![PyVISA](https://img.shields.io/badge/instrument-PyVISA-blue.svg)
![AI-Assisted](https://img.shields.io/badge/Development-AI--Assisted-purple)
[![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

> **Note:** This project is heavily based on code originally written by **[David](https://github.com/sansanda/pymeasure/blob/dev/tek371A/pymeasure/instruments/tektronix/tek371A.py)**.

This repository has all the commands and functions necessary to control the Tektronix TEK371 high power curve tracer using [PyVISA](https://pyvisa.readthedocs.io/). Its intended use is to perform I-V curves of power semiconductor devices, even though the equipment is capable of much more. The functions to control other aspects rather than the I-V curves are implemented, but not tested.

> **Note:** As for version 0.1.0, the controller only works if it is the only equipment controlling the SRQ line of the GPIB bus. If other equipments connected to the same bus hold the SRQ line the controller will not detect the end of a sweep measurement.

---
## **Features**
- Control Tektronix TEK371 via GPIB using PyVISA.
- Perform automated I-V curve measurements for power semiconductors.
  
---
## **Requirements**
- Python 3.10 (not tested with other versions)
- [PyVISA](https://pyvisa.readthedocs.io/)
- GPIB interface (e.g., NI GPIB-USB adapter)

---
## **Usage**
See [test](tests/test_diode.py) for a script to perform any number of consecutive I-V measurements of a power diode.

---
## **Development**

- This project was developed with AI assistance (M365 Copilot) for code suggestions, debugging, and optimization.

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

---
## Acknowledgments

- I would like to acknowledge **[David](https://github.com/sansanda/pymeasure/blob/dev/tek371A/pymeasure/instruments/tektronix/tek371A.py)** for the original implementation that served as the foundation for this project.

---
## Author

[Miquel Tutusaus](https://github.com/mtutusaus), 2025
