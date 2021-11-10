![](gui_assets/OSSAT-LOGO-BLACK.jpg)
# Mercury-GS
An Open Source Ground Station Terminal. 

For those who are new to the Space Industry and it's terminology, please refer to the [Background](#Background) section.
Also refer to the [OSSAT Glossary](/OSSAT%20Glossary.pdf) for explanations of any terminology.
Otherwise head to [User Setup](#user-setup) if you want to use the software, or [Development Setup](#development-setup) if you want to develop.

**NOTE: This software is not representative of what would be used for a real mission. 
It's intent is only for testing in a lab environment.**

## Contents
- [Background](#background)
- [Manual](#manual)
- [Setup](#setup)
  - [User Setup](#user-setup)
  - [Development Setup](#development-setup)
  - [Serial Comms Setup](#serial-comms-setup)
- [Creating Test Frames](#creating-test-frames)
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

## Manual
The manual, which describes how to use Mercury GS, is located in the repo [here](/Mercury%20GS%20Manual.docx).

**NOTE: This initial version of Mercury GS only fully supports Windows. 
Linux and MacOS support is expected after further development.** 

# Setup Guides
## User Setup
Install [Python3](https://www.python.org/downloads/).

Clone the repository onto your machine. Click the "Clone" button on the Github page.

In the [scripts](../scripts) folder are a number of scripts used to build the Python environment and run Mercury GS

WINDOWS:

Run the batch file [build_env.bat](../scripts/build_env.bat), you only need to do this once.
Then execute [run_env.bat](../scripts/run_env.bat) when you want to run MercuryGS.

UNIX/MACOS:

Run the shell script [build_env.sh](../scripts/build_env.sh), you only need to do this once.
Then execute [run_env.sh](../scripts/run_env.sh) when you want to run MercuryGS.

To communicate with Mercury GS via a terminal, emulating the link to a Spacecraft, follow the steps in [Serial Comms Setup](#serial-comms-setup).

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

**NOTE: For further information, design and requirements. You can find the Specification for Mercury GS [here](/OSSAT%20Mercury%20GS%20Specification_08.pdf).**

## Serial Comms Setup
The low level drivers talk over a COM port that is configurable in the GUI. To emulate a connection with a SpaceCraft we must spoof a connection between two ports.
Download a program like [HHD Virtual Serial Port Tools](https://freevirtualserialports.com/), create a virtual pair between two ports (for example COM1 and COM2), and then open a terminal program like [TeraTerm](https://ttssh2.osdn.jp/index.html.en) to listen on one of them (COM2 for example). Settings are default 9600 baud, 8 data bits, 0 parity bits, 1 stop bit. The baudrate is configurable in the GUI on the "CONFIG" tab.

**NOTE: This solution is only for Windows.**

## Creating Test Frames
Frames can be sent to MercuryGS via a terminal, these are located in the [Test Frames](/test_frames) folder.
[HHD Free Hex Editor](https://www.hhdsoftware.com/free-hex-editor) was used to create these frames.

## Designing the GUI
If you wish to edit the GUI, you will need Qt Designer.  
For *Qt Designer* install, it's suggested to download package from [here](https://build-system.fman.io/qt-designer-download), it is used to edit the UI layout - [platform-comms-app.ui](platform-comms-app.ui)

## Building the GUI
To use the qt ui file from the Qt designer, we need to build it to a python file.
You can do that by running: `pyuic5 platform-comms-app.ui -o platform_comms_app.py`
Or by running the build script from the "scripts" directory.
The built code of the current version of Mercury GS is included in the repo, so you will only need to rebuild the GUI if you make changes to it
To run the files built by the last step, run "main.py" either via command line or through a Python compatible IDE
