import logging
from commands import getstatusoutput
import os
import ciconf

class CIPlace(object):
    def __init__(self):
        super(CIPlace, self).__init__()

        self.name = None
        self.ap_name = []
        self.close_app_list = []
        self.open_app_list = []
        
    def close_app(self):
        logging.debug('Closing apps...')
        for app in self.close_app_list:
            ret = app.close()
            if not ret:
                logging.error('Failed to close app: %s' % app.name)

    def open_app(self):
        logging.debug('Opening apps...')
        for app in self.open_app_list:
            ret = app.open()
            if not ret:
                logging.error('Failed to open app: %s (%s)' % (app.name, app.path))

    def execute_script(self, script_type):
        script_path = '%s/%s.%s.sh' % (ciconf.SCRIPT_PATH, script_type, self.name)
        if os.path.isfile(script_path):
            cmd = '/bin/bash %s' % script_path
            (ret, out) = getstatusoutput(cmd)

    def checkin(self):
        self.execute_script('checkin')
        self.close_app()
        self.open_app()

    def checkout(self):
        self.execute_script('checkout')

    def dump(self):
        print 'ap_name = %s' % self.ap_name
        print 'open_app_list ='
        for app in self.open_app_list:
            print '\t' + app.name
        print 'close_app_list ='
        for app in self.close_app_list:
            print '\t' + app.name
