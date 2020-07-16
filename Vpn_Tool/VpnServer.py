import json
import socket
import platform
import os
import argparse
from subprocess import run


class VpnServer():
    def __init__(self):
        # if congif_file is None:
        #     self.config = None
        # else:
        #     self.config = congif_file
        self.system = platform.system()

    def generate_config_file(self, country='blank', password='FlightFinder', port=9090):
        try:
            hostname = socket.gethostbyname(socket.gethostname())
        except:
            hostname = '0.0.0.0'
        config_json = json.dumps(
            {
                # "name":country,
                "server":hostname,
                "server-port":port,
                "password":password,
                "timeout":60,
                "method":"aes-256-gcm"

            }
        )
        if self.system == 'Windows':
            directory='sample_configs'
        elif self.system == 'Linux':
            directory=os.path.join('/','etc','shadowsocks-libev')

        # file_name = "ssServerConfig_{country}.json".format(country=country)
        file_name='config.json'
        with open(os.path.join(directory,file_name), 'w') as conf_j:
            conf_j.write(config_json)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Start the shadowsocks server")
    parser.add_argument('--country',dest='country', type=str, default=None)
    args = parser.parse_args(['--country','usa'])

    vpn_server = VpnServer()
    vpn_server.generate_config_file(country=args.country)

    vpn_server = VpnServer()
    vpn_server.generate_config_file()


