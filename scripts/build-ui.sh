mv ../platform-comms-app.ui ./
pyuic5 platform-comms-app.ui -o platform_comms_app.py
mv platform_comms_app.py ../ -f
mv platform-comms-app.ui ../ -f