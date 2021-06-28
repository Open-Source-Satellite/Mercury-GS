# Mercury-GS

- [Mercury-GS](#mercury-gs)
  - [Development Setup](#development-setup)
  - [Serial Comms Setup](#serial-comms-setup)
  - [Sending And Receiving](#sending-and-receiving)
  - [Designing The GUI](#designing-the-gui)
  - [Building the GUI](#building-the-gui)

## Development Setup

A minimal Python 3 installation is required, it is recommended to use [*virtualenv*](https://pypi.org/project/virtualenv/) for clean Python installation and then install [PyQt](https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html) bindings:

```bash
python3 -m venv venv
source venv/bin/activate # or "call venv\Scripts\activate.bat" on Windows for initialize virtual environment
```
Make sure the following packages have been installed.
```bash
#PyQt5
python3 -m pip install PyQt5
# pyserial
python3 -m pip install pyserial
# PyQt5-tools
python3 -m pip install PyQt5-tools
# QtPy
python3 -m pip install QtPy
```
Another solution is to install a full Python IDE like [Pycharm](https://www.jetbrains.com/pycharm/) and install the packages through it's package manager.

## Serial Comms Setup
The low level drivers talk over COM port 19. To emulate a connection with a SpaceCraft we must spoof a connection between two ports.
Download a program like [com0com](http://com0com.sourceforge.net/), create a virtual pair between COM19 and COM20, and then open a terminal program like TeraTerm to listen on COM20. Settings are default 9600 baud, 8 data bits, 0 parity bits, 1 stop bit. The baudrate is configurable in the GUI on the "CONFIG" tab.

## Sending and Receiving
A telemetry request can be sent by typing the requested channel into the "Channel #" box and hitting "Send TLM REQ". The request is then packetised in the frameformat denoted in the spec and sends it over COM19. This should show on TeraTerm over COM20.
To send a message back, on TeraTerm click "File -> Send File" and navigate to the "Test Frames" folder within the repo. Select "Telemetry Request" and make sure that the "Binary" box is ticked before pressing "Open". This should send a formatted frame back to Mercury GS over COM20 -> COM19. The frame is then parsed and then displayed as a value of 1 under the "Telemetry" Section of the GUI under TLM CH 1.
I used [HHD Free Hex Editor](https://www.hhdsoftware.com/free-hex-editor) to create these "Test Frames".



## Designing the GUI
If you wish to edit the GUI, you will need Qt Designer.  
For *Qt Designer* install, it's suggested to download package from [here](https://build-system.fman.io/qt-designer-download), it is used to edit the UI layout - [platform-comms-app.ui](platform-comms-app.ui)

## Building the GUI
To use the qt ui file from the Qt designer, we need to build it to a python file.
You can do that by running: `pyuic5 platform-comms-app.ui -o platform_comms_app.py`
Or by running the build script from the "scripts" directory.
The built code of the current version of Mercury GS is included in the repo, so you will only need to rebuild the GUI if you make changes to it
To run the files built by the last step, run "main.py" either via command line or through a Python compatible IDE