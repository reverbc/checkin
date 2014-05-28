class CIApp(object):
    def __init__(self, name, path='', event_name=''):
        self.name = name
        self.path = '/Applications/'
        self.event_name = name
        if path.startswith('/'):
            self.path = path
        else:
            import os
            self.path = os.path.join(self.path, path)

        if event_name:
            self.event_name = event_name

    def open(self, force_open=False):
        import logging

        logging.debug('Opening app [%s]...' % self.name)
        if not self.is_running() or force_open:
            from commands import getstatusoutput
            import os
            postfix = '.app'
            if self.name.endswith(postfix):
                postfix = ''
            full_path = os.path.join(self.path, self.name)
            cmd = 'open \"%s%s\"' % (full_path, postfix)
            (ret, out) = getstatusoutput(cmd)
            logging.debug('Done.')
            return ret == 0
        return True

    def close(self, force_close=False):
        import logging

        logging.debug('Closing app [%s]...' % self.name)
        if self.is_running() or force_close:
            from commands import getstatusoutput
            cmd = 'osascript -e \'tell application \"%s\" to quit\'' % self.name
            (ret, out) = getstatusoutput(cmd)
            logging.debug('Done.')
            return ret == 0
        return True

    def is_running(self):
        import logging

        from commands import getstatusoutput
        cmd = 'osascript -e \'tell application "System Events" to (name of processes) contains \"%s\"\'' % self.event_name
        (ret, out) = getstatusoutput(cmd)
        result = ret == 0 and out == 'true'
        logging.debug('Event [%s] is running? %s' % (self.event_name, str(result)))
        return result