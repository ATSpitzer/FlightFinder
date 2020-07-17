import sys

from Vpn_Tool.VpnServer import VpnServer
from Vpn_Tool.VpnClient import VpnClient
import os
import platform
import argparse
import json
import subprocess
import pandas

class VpnTool():
    def __init__(self):
        os_system = platform.system()
        if os_system == 'Windows':
            self.config_dir="sample_configs"
        elif os_system == 'Linux':
            self.config_dir = os.path.join('/','etc','shadowsocks-libev')

        parser = argparse.ArgumentParser("""Tool for starting and stopping VPN (mostly client). Options:
        \tlist_servers \t- list countries of available VPN servers (-v verbose)
        \tadd_servers  \t- create a client config file for a new server (-c country -a public-ip-address)
        \tstart_server \t- start client pointed at server with country (-c country)
        \tstop_server  \t- stop client pointed at server with country (-c country [default: all])
        \tstatus_server\t- status of client pointed at server with country (-c country [default: all])""")
        parser.add_argument('command',type=str, help='Command to run')
        args = parser.parse_args(sys.argv[0:1])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def add_server(self):
        # print('adding server')
        parser = argparse.ArgumentParser("Create a client config for a vpn server")
        parser.add_argument('--country', '-c', required=True, dest='country', type=str)
        parser.add_argument('--address', '-a', required=True, dest='address', type=str)
        parser.add_argument('--config-dir', dest='config_dir', required=False, default=self.config_dir)
        args = parser.parse_args(sys.argv[1:])

        address = getattr(args, 'address')
        country=getattr(args,'country')
        config_dir=getattr(args,'config_dir')
        print("Server at {a} located in {c}".format(a=address, c=country))
        VpnClient.generate_config_file(server=address,country=country,config_dir=config_dir)

    def list_servers(self):
        country_options=VpnClient.load_configs(config_dir=self.config_dir)
        parser = argparse.ArgumentParser("Print list of vpn servers")
        parser.add_argument('-v',dest='verbose', action='store_true',help='Print out contents of all available client configs')
        args = parser.parse_args(sys.argv[1:])
        if getattr(args, 'verbose'):
            print(pandas.read_json(json.dumps(country_options)))
        else:
            print(*country_options.keys())

    def start_server(self):
        parser = argparse.ArgumentParser("Start the vpn client with a connection to the specified country")
        parser.add_argument('--country', '-c', required=True, dest='country', type=str, help="Country of vpn server. For a list of options run: python3 vpn_tool.py list_servers")
        args = parser.parse_args(sys.argv[1:])
        VpnClient().start_vpn(country=getattr(args,'country'))

    def stop_server(self):
        parser = argparse.ArgumentParser("Stop the vpn client with a connection to the specified country")
        parser.add_argument('--country', '-c', dest='country', type=str, default='all', help="Country of vpn server. For a list of options run: python3 vpn_tool.py list_servers")
        args = parser.parse_args(sys.argv[1:])
        VpnClient().stop_vpn(country=getattr(args,'country'))

    def status_server(self):
        parser = argparse.ArgumentParser("Status the vpn client with a connection to the specified country")
        parser.add_argument('--country', '-c', dest='country', type=str, default='all', help="Country of vpn server. For a list of options run: python3 vpn_tool.py list_servers")
        args = parser.parse_args(sys.argv[1:])
        VpnClient().status_vpn(country=getattr(args,'country'))

if __name__ == '__main__':
    if len(sys.argv)<=1 and platform.system()=='Windows':
        # sys.argv = ['add_server', '-a','123.456.789.230','-c','uk','-h']
        # sys.argv = ['list_servers','-v']
        sys.argv = ['-h']
    VpnTool()