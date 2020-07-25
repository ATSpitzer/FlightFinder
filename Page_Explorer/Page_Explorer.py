from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
import platform
import time
from datetime import date
from Vpn_Tool.VpnClient import VpnClient
import json
import os

class PageExplorer():

    def __init__(self, start_url="http://www.edreams.com", driver_element=None, country=None, no_cookies=False):
        if driver_element:
            print("Existing driver found")
            self.driver = driver_element
        else:
            os_system = platform.system()
            if os_system == 'Windows':
                options = webdriver.ChromeOptions()
                options.add_experimental_option("detach", True)
                # options.add_argument('headless')
                self.driver = webdriver.Chrome("C:\chromedriver.exe", options=options)
                self.driver.maximize_window()
            elif os_system == 'Linux':
                config_dir = os.path.join('/','etc','shadowsocks-libev')
                fp = webdriver.FirefoxProfile()
                if country is None:
                    socks_port = 1080
                else:
                    vpn = VpnClient(country)
                    socks_port = vpn.config_options[country]['local_port']
                    if vpn.status_vpn().returncode != 0:
                        vpn.start_vpn()

                fp.set_preference('network.proxy.type', 1)  # int
                fp.set_preference('network.proxy.socks', '127.0.0.1')  # string
                fp.set_preference('network.proxy.socks_port', socks_port)  # int
                fp.set_preference('network.proxy.socks_version', 5)
                options = webdriver.firefox.options.Options()
                options.headless = True
                self.driver = webdriver.Firefox(options=options, firefox_profile=fp)
            if no_cookies:
                self.driver.delete_all_cookies()
            self.driver.get(start_url)


        #Just wait 1 second since it may take a moment for page to properly load
        time.sleep(1)
        #
        # self.service_country = os.getenv('COUNTRY_SERVICE','usa')
        #
        # self.initial_page_setup()

    def get_driver_object(self):
        return self.driver

    def check_url(self, screenshot=False, screenshot_name=None):
        title = self.driver.title
        url = self.driver.current_url
        print("URL: {cur_url}\tTitle: {title}".format(cur_url=url, title=title))

        if screenshot:
            if screenshot_name is None:
                screenshot_name = "screen_at_{d}_{t}.png".format(t=time.time(), d=date.today().isoformat())
            self.driver.save_screenshot(filename=screenshot_name)
        return url

    def close_driver(self):
        self.driver.close()

    def kill_driver(self):
        self.driver.quit()