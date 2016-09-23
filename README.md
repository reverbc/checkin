Check In
========

This is a small tool for Mac that will automatically do something when changing to different wireless work - i.e. connecting to different AP. 

Prerequisite
------------

1. Install `terminal-notifier` from [alloy/terminal-notifier](https://github.com/alloy/terminal-notifier)

Installation
------------

1. Clone the code to your local machine
2. Modify application configuration and save it to `conf/application.conf`
3. Modify location definition and desired action and save it to `conf/location.YOUR_LOCATION_NAME.conf`
4. Make checkin.py as an executable script: `chmod +x /PATH/TO/PROJECT/checkin/checkin.py`
5. Modify `CONF_PATH` variable in `lib/ciconf.py` 
6. Put `com.reverbhorn.checkin.plist` into `~/Library/LaunchAgents/` and point the `ProgramArguments` variable in plist to your checkin executable path
7. Execute `launchctl load ~/Library/LaunchAgents/com.reverbhorn.checkin.plist 
8. Done!

Application Configuration (application.conf)
--------------------------------------------

Place your application definition here.

The format of the file is:
```
Format: APP_NAME, EVENT_NAME, PATH, IS_PERMANENT
    APP_NAME: file name of app (REQUIRED)
        - Example: Mail.app -> Mail
    EVENT_NAME: event name inside Systen Event (OPTIONAL)
        - If empty: APP_NAME will be used
    PATH: path to application's parent folder if needed (OPTIONAL)
        - If empty: uses "/Application/"
        - If starts with /: uses absolutely path
        - If starts without /: uses relatively path to /Application/
    IS_PERMANENT: should this app be opened at all time (REQUIRED)
        - True/False
```

Location Configuration (location.*.conf)
----------------------------------------

Place your location definition here.

Each location can have multiple AP name, and of course you can have multiple location definition file.

File format as following:
```
AP_NAME=AP_1, AP_2
CLOSE_APP=APP_1, APP_2, APP_3
OPEN_APP=APP_4, APP_5, APP_6
OPEN_PERMANENT=True|False
CLOSE_PERMANENT=True|False
```
- AP_NAME: The name list of AP, separate by comma
- CLOSE_APP: The name list of application which you want to close when arriving this location, separate by comma
- OPEN_APP: The name list of application which you want to open when arriving this location, separate by comma
- OPEN_PERMANENT: Set this flag to open all the "permanent" applications which defined in application.conf **CANNOT SET WITH CLOSE_PERMANENT**
- CLOSE_PERMANENT: Set this flag to close all the "permanent" applications which defined in application.conf **CANNOT SET WITH OPEN_PERMANENT**

License
-------

Copyright (c) 2014 Reverb Chu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
