import os
import platform
import json
import subprocess

class VpnClient():
    def __init__(self, country=None):
        os_system = platform.system()
        if os_system == 'Windows':
            self.config_dir="sample_configs"
        elif os_system == 'Linux':
            self.config_dir = os.path.join('/','etc','shadowsocks-libev')

        ss_configs = os.listdir(self.config_dir)
        self.config_options = VpnClient.load_configs(self.config_dir)
        self.country = None
        if country is not None:
            self.set_country(country)

    # def load_configs(self, ss_configs):
    #     def check_configs(self, config, config_name):
    #         config_contents = json.load(config)
    #         if "name" in config_contents.keys():
    #             config_country=config_contents["name"]
    #             self.config_options[config_country] = config_contents
    #             self.config_options[config_country]["path"] = config_name.replace('.json','')
    #
    #     for f in ss_configs:
    #         with open(os.path.join(self.config_dir, f), 'r') as config_file:
    #             check_configs(self, config_file, f)

    @staticmethod
    def add_config(config, config_name, config_options):
        """
        Takes a config json and checks if it has a name field. If so it adds it to the list of vpn options

        :param config: string representation of the contents of a json file
        :param config_name:  string of the filename of the checked config
        :param config_options:  dictionary of checked files
        :return: dictionary updated with the checked file
        """
        config_contents = json.load(config)
        if "name" in config_contents.keys():
            config_country=config_contents["name"]
            config_options[config_country] = config_contents
            config_options[config_country]["path"] = config_name.replace('.json','')
        return config_options

    @staticmethod
    def load_configs(config_dir):
        """
        List valid vpn client configs in a directory
        :param config_dir:  directory to check
        :return: dictionary containing valid config files by country
        """
        config_options = {}
        for filename in os.listdir(config_dir):
            with open(os.path.join(config_dir, filename), 'r') as config_file:
                VpnClient.add_config(config_file, filename, config_options)
        return config_options


    def set_country(self, country):
        """
        :param country: Set or change the country the VpnServer will start/stop/status
        :return:
        """
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

    @staticmethod
    def generate_config_file(server, country, config_dir, password='FlightFinder', server_port=9090, local_port=1080):
        """
        :param server: Public IP of the VPN server client will point to
        :param country:  Country the VPN server will point to
        :param config_dir: Location of config file should be /etc/shadowsocks-libev
        :param password: Password to connect to VPN
        :param server_port:  VPN server port
        :param local_port: Port for local machine
        :return:
        """
        assert server is not None or country is not None, "Country and server address must be set"
        config_json = json.dumps(
            {
                "name":country,
                "server":server,
                "server_port":server_port,
                "password":password,
                "local":"127.0.0.1",
                "local_port":local_port,
                "fast_open":False,
                "timeout":60,
                "method":"aes-256-gcm"

            }
        )

        file_name = "ssClientConfig_{country}.json".format(country=country)
        with open(os.path.join(config_dir,file_name), 'w') as conf_j:
            conf_j.write(config_json)