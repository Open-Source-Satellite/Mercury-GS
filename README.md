# Mercury-GS
An Open Source Ground Station Terminal. 

For those who are new to the Space Industry and it's terminology, please refer to the [Background](#Background) section. 
Otherwise head to [User Guide](#user-guide) if you want to use the software, or [Development Setup](#development-setup) if you want to develop.

## Contents
- [User Guide](#user-guide)
  - [Setup](#setup)
- [Development Setup](#development-setup)
  - [Serial Comms Setup](#serial-comms-setup)
  - [Sending And Receiving](#sending-and-receiving)
  - [Designing The GUI](#designing-the-gui)
  - [Building the GUI](#building-the-gui)

## Background
Once a Spacecraft is in flight, operators will need to communicate with it. 
This is normally facilitated via Ground Stations located around the globe that use a radar dish to send and receive packets of data.

During a typical mission, a Spacecraft will send stats down to the ground, which we call Telemetry.
This could be temperature, battery charge, sensor readings, or any data point that you can think of.
However, the Spacecraft would usually only transmit the most important Telemetry by itself due to limitations with the radio link. 
The Ground Station can request for a particular Telemetry point by sending a Telemetry Request.

The Ground Station doesn't just monitor a Spacecraft's Telemetry, an operator can send commands to tell it to do things.
This could be switching on a particular gadget, turning towards the Sun to charge batteries, 
synchronising the on-board time to the Ground or a variety of mission specific functions.
These are facilitated by something called a Telecommand.

It is also required to upload and download files. This could be downloading images taken by a camera on the payload of the Spacecraft
, or uploading an Operational Timetable or code update to the Spacecraft.

### User Guide
## Setup
Install [Python3](https://www.python.org/downloads/).

Clone the repository onto your machine. Click the "Clone" button on the Github page.

In the [scripts](../scripts) folder are a number of scripts used to build the Python environment and run Mercury GS

WINDOWS:

Run the batch file [build_env.bat](../scripts/build_env.bat), you only need to do this once.
Then execute [run_env.bat](../scripts/run_env.bat) when you want to run MercuryGS.

UNIX/MACOS:

Run the shell script [build_env.sh](../scripts/build_env.sh), you only need to do this once.
Then execute [run_env.sh](../scripts/run_env.sh) when you want to run MercuryGS.

## Development Setup

A minimal [Python3](https://www.python.org/downloads/) installation is required, it is recommended to use [*virtualenv*](https://pypi.org/project/virtualenv/) for clean Python installation and then install [PyQt](https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html) bindings.
You can either run the scripts as shown in [Setup](#setup) or manually like so: 


1) Clone the repo and navigate to it's directory.

2) Create a new virtual environment
```bash
python -m venv MercuryGSEnv
```
2) Activate the virtual environment...

For WINDOWS:
```batch
call MercuryGSEnv\Scripts\activate.bat
```
For LINUX/MAC:
```bash
source MercuryGSEnv/bin/activate
```
3) Install the required packages
```bash
pip install -r requirements.txt
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
The low level drivers talks over a COM port that is configurable in the GUI. To emulate a connection with a SpaceCraft we must spoof a connection between two ports.
Download a program like [HHD Virtual Serial Port Tools](https://freevirtualserialports.com/), create a virtual pair between COM1 and COM2, and then open a terminal program like [TeraTerm](https://ttssh2.osdn.jp/index.html.en) to listen on COM2. Settings are default 9600 baud, 8 data bits, 0 parity bits, 1 stop bit. The baudrate is configurable in the GUI on the "CONFIG" tab.

## Sending and Receiving
A telemetry request can be sent by typing the requested channel into the "Channel #" box and hitting "Send TLM REQ". The request is then packetised in the frameformat denoted in the spec and sends it over COM1. This should show on TeraTerm over COM2.
To send a message back, on TeraTerm click "File -> Send File" and navigate to the "Test Frames" folder within the repo. Select "Telemetry Request" and make sure that the "Binary" box is ticked before pressing "Open". This should send a formatted frame back to Mercury GS over COM2 -> COM1. The frame is parsed and then displayed as a value of 1 under the "Telemetry" Section of the GUI under TLM CH 1.
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
