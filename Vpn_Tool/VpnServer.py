import json
import socket
import platform
import os
import subprocess

class VpnServer():
    def __init__(self):
        os_system = platform.system()
        if os_system == 'Windows':
            self.config_dir="sample_configs"
        elif os_system == 'Linux':
            self.config_dir = os.path.join('/','etc','shadowsocks-libev')

    def generate_config_file(self, password='FlightFinder', port=9090):
        try:
            hostname = socket.gethostbyname(socket.gethostname())
        except:
            hostname = '0.0.0.0'
        config_json = json.dumps(
            {
                "server":hostname,
                "server_port":port,
                "local_port": 1080,
                "password":password,
                "timeout":60,
                "method":"aes-256-gcm"

            }
        )
        file_name='config.json'
        with open(os.path.join(self.config_dir,file_name), 'w') as conf_j:
            conf_j.write(config_json)

    def start_vpn(self):
        command_string = "sudo systemctl start shadowsocks-libev.service"
        completed=subprocess.run(command_string,  shell=True, check=True, stdout=subprocess.PIPE )
        return completed

    def enable_vpn(self):
        command_string = "sudo systemctl enable shadowsocks-libev.service"
        completed=subprocess.run(command_string,  shell=True, check=True, stdout=subprocess.PIPE )
        return completed

    def status_vpn(self):
        command_string = "sudo systemctl status shadowsocks-libev.service"
        completed=subprocess.run(command_string,  shell=True, check=True, stdout=subprocess.PIPE )
        return completed

    def restart_vpn(self):
        command_string = "sudo systemctl restart shadowsocks-libev.service"
        completed=subprocess.run(command_string,  shell=True, check=True, stdout=subprocess.PIPE )
        return completed

if __name__ == '__main__':
    vpn = VpnServer()
    vpn.generate_config_file()
    print('\n. . . . . . . . . . . . . . . \n')
    print(vpn.start_vpn())
    print('\n. . . . . . . . . . . . . . . \n')
    print(vpn.enable_vpn())
    print('\n. . . . . . . . . . . . . . . \n')
    print(vpn.restart_vpn())
    print('\n. . . . . . . . . . . . . . . \n')
    print(vpn.status_vpn())
    print('\n. . . . . . . . . . . . . . . \n')


