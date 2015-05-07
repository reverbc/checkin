#!/usr/bin/python
from lib import ciplaces
from lib import ciutils
from lib import ciconf
import logging

IS_DEBUG = False

def init():
    global IS_DEBUG

    if IS_DEBUG:
        log_level = logging.DEBUG
        log_file = None
    else:
        log_level = logging.INFO
        log_file = ciconf.LOG_FILE

    # NOTE: to enable module/method tracking: add '[%(module)s.%(funcName)s]'
    logging.basicConfig(filename=log_file, level=log_level, datefmt='%Y.%m.%d %H:%M:%S', 
                        format='%(asctime)s [%(levelname)s]\t%(message)s')

def load_last_ap():
    latest_ap = ''
    try:
        config = open(ciconf.LATEST_AP, 'r')
        latest_ap = config.read()
        config.close()
    except Exception, ex:
        logging.error('Failed to load last AP: %s' % str(ex))
    return latest_ap

def update_last_ap(latest_ap):
    logging.debug('Updating latest AP: %s' % latest_ap)
    config = open(ciconf.LATEST_AP, 'w')
    config.write(latest_ap)
    config.close()

def show_notification(current_ap, ip, current_location):
    from commands import getstatusoutput
    cmd = '/usr/local/bin/terminal-notifier -title \"Check In\"'
    cmd += ' -subtitle \"%s (%s)\"' % (current_ap, ip)
    cmd += ' -message \"just checked in at %s.\"' % current_location
    (ret, out) = getstatusoutput(cmd)

def go():
    location_list = ciplaces.get_instance().get_place_list()

    last_ap = load_last_ap()
    current_ap = ciutils.get_ap_name()
    current_location = 'nowhere'

    if not current_ap:
        logging.info('No connection...bye.')
        return 0

    ip = ciutils.get_current_ip()
    if ip == '127.0.0.1':
        logging.info('No IP assigned. Keep sleeping...')
        return 0
    elif last_ap == current_ap:
        logging.info('I am not connecting to different AP...bye :)')
    else:
        logging.info('Changing AP from [%s] to [%s].' % (last_ap, current_ap))
        for location in location_list.keys():
            if current_ap in location_list[location].ap_name:
                location_list[location].i_am_here()
                current_location = location
            elif last_ap in location_list[location].ap_name:
                location_list[location].leaving_here()
        if not current_location:
            logging.warning('Current AP is not recorded.')
        show_notification(current_ap, ip, current_location)

    update_last_ap(current_ap)
    logging.info('Currently connecting to AP [%s] with IP [%s]' % (current_ap, ip))
    return 0

if __name__ == '__main__':
    init()
    go()