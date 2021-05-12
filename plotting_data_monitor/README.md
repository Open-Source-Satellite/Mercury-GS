## Plotting Data Monitor

A good example of a pair of Python scripts, one which writes to a serial port and a second which reads from a serial port and presents the data in a GUI.

Orginally taken from&nbsp;
 https://eli.thegreenplace.net/2009/08/07/a-live-data-monitor-with-python-pyqt-and-pyserial/&nbsp;
Sources at
 https://github.com/eliben/code-for-blog/tree/master/2009/plotting_data_monitor

Also uses serialutils.py and utils.py from
 https://github.com/eliben/code-for-blog/tree/master/2009/eblib



Modified for Python 3, PyQt5 and to use QProgressBar instead of qwtthermo.

Currently only working on Windows (can be modified for Linux)

Requires Python serial, PyQt5 and PythonQwt modules

On Windows:&nbsp;
 python -m pip install pyserial&nbsp;
 python -m pip install PyQt5&nbsp;
 python -m pip install PythonQwt


To simulate two serial ports use com0com&nbsp;
https://sourceforge.net/projects/com0com/files/com0com/3.0.0.0/com0com-3.0.0.0-i386-and-x64-signed.zip/download

Com0com will create two virtual serial ports, such as COM4 and COM5.

sender_sim.py is currently hard coded to use COM4, modify it if necessary.

To use:&nbsp;
 start sender_sim.py&nbsp;
 start plotting_data_monitor.pyw&nbsp;
 from the menu select File, Select COM Port&nbsp;
 choose the virtual COM port created by com0com which is not in use by sender_sim.py&nbsp;
 select File, Start monitor


