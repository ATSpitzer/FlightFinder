from Vpn_Tool.VpnServer import VpnServer
from Vpn_Tool.VpnClient import VpnClient
import os
import platform
import argparse
import json
import subprocess

class VpnTool():
    def __init__(self):
        os_system = platform.system()
        if os_system == 'Windows':
            config_dir="sample_configs"
        elif os_system == 'Linux':
            config_dir = os.path.join('/','etc','shadowsocks-libev')



if __name__ == '__main__':
    # parser = argparse.ArgumentParser("Start the shadowsocks server")
    # parser.add_argument('--country',dest='country', type=str, default=None)
    # args = parser.parse_args(['--country','usa'])
    #
    # vpn_server = VpnServer()
    # vpn_server.generate_config_file(country=args.country)
    #
    # vpn_server = VpnServer()
    # vpn_server.generate_config_file()
    vc = VpnClient()