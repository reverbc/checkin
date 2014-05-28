def get_ap_name():
    ap_name = None
    try:
        from commands import getstatusoutput
        cmd = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport -I | grep " SSID"'
        (ret, out) = getstatusoutput(cmd)
        ap_name = out.split(':')[1].strip()
    except:
        pass
    return ap_name

def get_current_ip():
    import socket
    return socket.gethostbyname(socket.gethostname())

if __name__ == '__main__':
    print get_ap_name()
