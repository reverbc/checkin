import os

from ciapp import CIApp
import logging
import ciconf

class CIApps(object):
    def __init__(self):
        super(CIApps, self).__init__()
        self._app_list = None
        self._papp_list = None
        self.init_app_list()
        
    def add_app(self, app_name, event_name='', path='', is_permanent=False):
        if not app_name:
            print('Name of application cannot be empty/None.')
            return False
        if app_name in self._app_list.keys():
            print('Application with same name has already been created.')
            return False

        app = CIApp(app_name, event_name=event_name, path=path)
        self._app_list[app_name] = app

        if is_permanent:
            self._papp_list.append(app)

        return True

    def del_app(self, app_name=''):
        if not app_name:
            print('Name of application cannot be empty/None.')
            return False
        if not app_name in self._app_list.keys():
            print('Application does not exist.')
            return False

        for papp in self._papp_list:
            if app_name == papp.name:
                self._papp_list.remove(papp)
        del self._app_list[app_name]

    def list_app(self):
        print 'App Name\t|\tEvent Name\t|\tPath'
        for app in self._app_list:
            print '%s\t|\t%s\t|\t%s' % (app, self._app_list[app].event_name, self._app_list[app].path)
        print ''
        print 'App Name\t|\tEvent Name\t|\tPath'
        for app in self._papp_list:
            print '%s\t|\t%s\t|\t%s' % (app.name, app.event_name, app.path)
        print ''

    def get_permanent_apps(self):
        return self._papp_list

    def get_app(self, app_name):
        if not app_name in self._app_list.keys():
            logging.error('No app found from name: [%s]' % app_name)
            return None
        return self._app_list[app_name]

    def init_app_list(self):
        self._app_list = dict()
        self._papp_list = list()

        app_conf_path = os.path.join(ciconf.CONF_PATH, ciconf.APP_CONF)
        try:
            with open(app_conf_path, 'r') as f:
                line = '#'
                while line:
                    if not line.startswith('#') and line.strip():
                        try:
                            app_entry = line.split(',')
                            self.add_app(app_entry[0], app_entry[1], app_entry[2], eval(app_entry[3]))
                        except Exception, ex:
                            logging.error('Failed to parse line (%s):\n\t-> %s' % (ex, str(line)))
                    line = f.readline()
        except IOError, ex:
            print 'Please initial [%s] before execute the script.' % app_conf_path
            import sys
            sys.exit()

__rrapp_instance__ = None
def get_instance():
    global __rrapp_instance__
    if __rrapp_instance__ is None:
        __rrapp_instance__ = CIApps()
    return __rrapp_instance__

if __name__ == '__main__':
    instance = get_instance()

    instance.list_app()
    #print instance.GoogleMusic.is_running()
    #print instance.GoogleMusic.open()

    #print instance.SafeSync.is_running()