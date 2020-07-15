import os
import platform
import json
import subprocess

class VpnClient():
    def __init__(self, country=None):
        os_system = platform.system()
        if os_system == 'Windows':
            config_dir="sample_configs"
        elif os_system == 'Linux':
            config_dir = os.path.join('/','etc','shadowsocks-libev')

        ss_configs = os.listdir(config_dir)
        print(ss_configs)

        self.config_options = {}

        def load_configs(self, config, config_name):
            config_contents = json.load(config)
            if "name" in config_contents.keys():
                config_country=config_contents["name"]
                self.config_options[config_country] = config_contents
                self.config_options[config_country]["path"] = config_name.replace('.json','')



        for f in ss_configs:
            with open(os.path.join(config_dir, f), 'r') as config_file:
                load_configs(self, config_file, f)

        self.country=None
        if country is not None:
            self.set_country(country)

    def set_country(self, country):
        cntry_list=self.get_options()
        assert country in self.get_options(), "Tried to set vpn to {cntry} but no config found. Try {cntry_list}".format(cntry=country, cntry_list=cntry_list)
        self.country = country

    def get_options(self):
        country_options = list(self.config_options)
        return country_options

    def stop_vpn(self, country=None):
        if country is None:
            if self.country is None:
                country = 'all'
            else:
                country = self.country

        if country is not None:
            if country == 'all':
                command_string = "sudo systemctl stop shadowsocks-libev-local@*.service"
            else:
                cntry_list = self.get_options()
                assert country in cntry_list, "No vpn config matches {cntry}, try {cntry}.list".format(cntry=country, cntry_list=cntry_list)
                command_string = "sudo systemctl stop shadowsocks-libev-local@{config_name}.service".format(config_name=self.config_options[country]['path'])
        completed=subprocess.run(command_string,  shell=True, check=True, stdout=subprocess.PIPE )
        return completed

    def start_vpn(self, country=None, safe=False):
        if country is None:
            assert self.country is not None, "No country set yet for vpn, set country or specify country to start vpn with"
            country = self.country

        if safe:
            self.stop_vpn()
        self.set_country(country)
        command_string = "sudo systemctl start shadowsocks-libev-local@{config_name}.service".format(config_name=self.config_options[country]['path'])
        completed=subprocess.run(command_string,  shell=True, check=True, stdout=subprocess.PIPE )
        return completed

    def status_vpn(self, country=None):
        if country is None:
            if self.country is None:
                country = 'all'
            else:
                country = self.country


        if country == 'all':
            command_string = "sudo systemctl status shadowsocks-libev-local@*.service"
        else:
            cntry_list = self.get_options()
            assert country in cntry_list, "No vpn config matches {cntry}, try {cntry}.list".format(cntry=country, cntry_list=cntry_list)
            command_string = "sudo systemctl status shadowsocks-libev-local@{config_name}.service".format(config_name=self.config_options[country]['path'])
        completed=subprocess.run(command_string,  shell=True, check=True, stdout=subprocess.PIPE )
        print(completed.stdout)
        return completed
