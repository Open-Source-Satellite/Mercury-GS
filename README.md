# Mercury-GS

- [Mercury-GS](#mercury-gs)
  - [Development Setup](#development-setup)
  - [Build](#build)

## Development Setup

A minimal Python 3 intallation is required, it is suggested to use [*virtualenv*](https://pypi.org/project/virtualenv/) for clean Python installation and then install [PyQt](https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html) bindings:

```bash
python3 -m venv venv
source venv/bin/activate # or "call venv\Scripts\activate.bat" on Windows for initialize virtual environment
python3 -m pip install PyQt5
```

For *Qt Designer* install, it's suggested to download package from [here](https://build-system.fman.io/qt-designer-download), it is used to edit the UI layout - [platform-comms-app.ui](platform-comms-app.ui)

[serial_framing](serial_framing/) includes logic for frame parsing of protocol, the folder includes some unit test cases for testing message parsing - [test_protocolwrapper.py](serial_framing/test_protocolwrapper.py)

## Build
To use the qt ui file from the Qt designer, we need to build it to a python file.
You can do that by running: `pyuic5 platform-comms-app.ui -o platform_comms_app.py`
Or by running the build script form the root of the project by running: `bash scripts/build-ui.sh`

## Running The GUI
To run the python built by the last step, run "main.py" either via command line or through a Python compatible IDE
