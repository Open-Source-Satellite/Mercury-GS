# Mercury-GS

- [Mercury-GS](#mercury-gs)
  - [Development Setup](#development-setup)
  - [Build](#build)
  - [Running The GUI](#running-the-gui)
  - [Serial Comms Setup](#serial-comms-setup)
  - [Sending And Receiving](#sending-and-receiving)

## Development Setup

A minimal Python 3 intallation is required, it is suggested to use [*virtualenv*](https://pypi.org/project/virtualenv/) for clean Python installation and then install [PyQt](https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html) bindings:

```bash
python3 -m venv venv
source venv/bin/activate # or "call venv\Scripts\activate.bat" on Windows for initialize virtual environment
python3 -m pip install PyQt5
```
It is recommended to check for the following packages and install them if missing
```bash
# pyserial
python3 -m pip install pyserial
# PyQt5-tools
python3 -m pip install PyQt5-tools
# QtPy
python3 -m pip install QtPy
```
For *Qt Designer* install, it's suggested to download package from [here](https://build-system.fman.io/qt-designer-download), it is used to edit the UI layout - [platform-comms-app.ui](platform-comms-app.ui)

## Build
To use the qt ui file from the Qt designer, we need to build it to a python file.
You can do that by running: `pyuic5 platform-comms-app.ui -o platform_comms_app.py`
Or by running the build script form the root of the project by running: `bash scripts/build-ui.sh`

## Running The GUI
To run the python built by the last step, run "main.py" either via command line or through a Python compatible IDE

## Serial Comms Setup
The low level drivers talk over COM port 19. To emulate a connection with a SpaceCraft we must spoof a connection between two ports.
Download a program like [com0com](http://com0com.sourceforge.net/), create a virtual pair between COM19 and COM20, and then open a terminal program like TeraTerm to listen on COM20. Settings are default 9600 baud, 8 data bits, 0 parity bits, 1 stop bit. The baudrate is configurable in the GUI on the "CONFIG" tab.

## Sending and Receiving
A telemetry request can be sent by typing the requested channel into the "Channel #" box and hitting "Send TLM REQ". The request is then packetised in the frameformat denoted in the spec and sends it over COM19. This should show on TeraTerm over COM20.
To send a message back, on TeraTerm click "File -> Send File" and navigate to the "Test Frames" folder within the repo. Select "Telemetry Request" and make sure that the "Binary" box is ticked before pressing "Open". This should send a formatted frame back to Mercury GS over COM20 -> COM19. The frame is then parsed and then displayed as a value of 1 under the "Telemetry" Section of the GUI under TLM CH 1.
I used [HHD Free Hex Editor](https://www.hhdsoftware.com/free-hex-editor) to create these "Test Frames".
