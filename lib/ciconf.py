import os

LATEST_AP = ''
LOG_FILE = ''
CONF_PATH = ''
SCRIPT_PATH = ''
APP_CONF = ''
NOTIFICATION_ICON = ''

conf_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'conf', 'checkin.conf'))
try:
    with open(conf_path) as conf:
        line = '#'
        while line:
            if not line.startswith('#') and line.strip():
                (key, value) = line.split('=')

                if key == 'LATEST_AP':
                    LATEST_AP = value.strip()
                elif key == 'LOG_FILE':
                    LOG_FILE = value.strip()
                elif key == 'CONF_PATH':
                    CONF_PATH = value.strip()
                elif key == 'SCRIPT_PATH':
                    SCRIPT_PATH = value.strip()
                elif key == 'APP_CONF':
                    APP_CONF = value.strip()
                elif key == 'NOTIFICATION_ICON':
                    NOTIFICATION_ICON = value.strip()
                else:
                    logging.warning('Undefined key [%s] from [%s]' % (key, place))
            line = conf.readline()
except IOError, ex:
    print 'Please initial [%s] before execute the script.' % conf_path
    import sys
    sys.exit()
