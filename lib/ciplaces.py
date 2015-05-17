#!/usr/bin/python
from ciplace import CIPlace
import ciconf
import ciapps
APP_LIST = ciapps.get_instance()

class CIPlaces(object):
    def __init__(self):
        super(CIPlaces, self).__init__()
        self._place_list = None
        self.init_place_list()

    def get_place_list(self):
        return self._place_list

    def _get_place_conf_list(self):
        import commands
        pl = commands.getstatusoutput('cd %s; ls location.*.conf 2>/dev/null' % ciconf.CONF_PATH)[1].split('\n')
        return pl

    def dump(self):
        for p in self._place_list:
            print '\n== %s ==' % p
            self._place_list[p].dump()

    def init_place_list(self):
        self._place_list = dict()
        pl = self._get_place_conf_list()

        for place in pl:
            if place:
                pname = place.split('.')[1]
                nl = CIPlace(pname)
                with open('%s/%s' % (ciconf.CONF_PATH, place)) as pconf:
                    line = '#'
                    while line:
                        if not line.startswith('#') and line.strip():
                            (key, value) = line.split('=')

                            if key == 'AP_NAME':
                                ap_list = value.split(',')
                                for ap in ap_list:
                                    nl.ap_name.append(ap.strip())
                            elif key == 'CLOSE_APP':
                                capp_list = value.split(',')
                                for app in capp_list:
                                    app = app.strip()
                                    if app:
                                        nl.close_app_list.append(APP_LIST.get_app(app))
                            elif key == 'OPEN_APP':
                                oapp_list = value.split(',')
                                for app in oapp_list:
                                    app = app.strip() 
                                    if app:
                                        nl.open_app_list.append(APP_LIST.get_app(app))
                            elif key == 'OPEN_PERMANENT':
                                if eval(value.strip()):
                                    nl.open_app_list = nl.open_app_list + APP_LIST.get_permanent_apps()
                            elif key == 'CLOSE_PERMANENT':
                                if eval(value.strip()):
                                    nl.close_app_list = nl.close_app_list + APP_LIST.get_permanent_apps()
                            else:
                                logging.warning('Undefined key [%s] from [%s]' % (key, place))

                        line = pconf.readline()
                    self._place_list[pname] = nl


__rrplace_instance__ = None
def get_instance():
    global __rrplace_instance__
    if __rrplace_instance__ is None:
        __rrplace_instance__ = CIPlaces()
    return __rrplace_instance__

if __name__ == '__main__':
    instance = get_instance()
    instance.dump()
