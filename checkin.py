#!/usr/bin/env python

from lib import ciconf
from lib import ciplaces
from lib import ciutils

import logging
import argparse
from commands import getstatusoutput

def init(is_debug):
    if is_debug:
        log_level = logging.DEBUG
        log_file = None
        module_info = '<<%(module)s.%(funcName)s>>'
    else:
        log_level = logging.INFO
        log_file = ciconf.LOG_FILE
        module_info = ''

    log_format = '%(asctime)s [%(levelname)s]\t%(message)s ' + module_info
    date_format = '%Y.%m.%d %H:%M:%S'

    logging.basicConfig(filename=log_file, level=log_level, datefmt=date_format, format=log_format)

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
    cmd = '/usr/local/bin/terminal-notifier -title \"Check In\"'
    cmd += ' -subtitle \"%s (%s)\"' % (current_ap, ip)
    cmd += ' -message \"just checked in at %s.\"' % current_location

    if ciconf.NOTIFICATION_ICON:
        cmd += ' -contentImage \"%s\"' % ciconf.NOTIFICATION_ICON

    (ret, out) = getstatusoutput(cmd)

def go(force=False):
    current_ap = ciutils.get_ap_name()
    
    if not current_ap:
        logging.info('No connection...bye.')
    else:
        location_list = ciplaces.get_instance().get_place_list()
        last_ap = load_last_ap()
        current_location = ciplaces.NOWHERE
        previous_location = ciplaces.NOWHERE

        ip = ciutils.get_current_ip()
        if ip == '127.0.0.1' and not force:
            logging.info('No IP assigned. Keep sleeping...')
        elif last_ap == current_ap and not force:
            logging.info('I am not connecting to different AP...bye :)')
        else:
            logging.info('Changing AP from [%s] to [%s].' % (last_ap, current_ap))
            for location in location_list.keys():
                if current_ap in location_list[location].ap_name:
                    current_location = location
                elif last_ap in location_list[location].ap_name:
                    previous_location = location

            if previous_location != ciplaces.NOWHERE:
                location_list[previous_location].checkout()
            if current_location != ciplaces.NOWHERE:
                location_list[current_location].checkin()

            show_notification(current_ap, ip, current_location)
            update_last_ap(current_ap)
            logging.info('Currently connecting to AP [%s] with IP [%s]' % (current_ap, ip))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', action='store_true', help='check in current location anyway')
    parser.add_argument('-d', '--debug', action='store_true', help='turn on debug mode')
    args = parser.parse_args()

    init(is_debug=args.debug)

    if args.debug:
        logging.debug('Running in debug mode...')
    if args.force:
        logging.info('Force running...')

    go(force=args.force)