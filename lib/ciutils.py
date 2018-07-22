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
    import subprocess
    cmd = "ifconfig en0 | grep 'inet\ ' | awk '{print $2;}'"
    return subprocess.check_output(cmd, shell=True).strip()


if __name__ == '__main__':
    print(get_ap_name())
