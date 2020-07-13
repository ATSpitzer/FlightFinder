from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import platform
import os
import time
from datetime import date

class PageExplorer():

    def __init__(self, start_url="http://www.edreams.com", driver_element=None):
        if driver_element:
            print("Existing driver found")
            self.driver = driver_element
        else:
            os_system = platform.system()
            if os_system == 'Windows':
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                self.driver = webdriver.Chrome("C:\chromedriver.exe", options=options)
                self.driver.maximize_window()
            elif os_system == 'Linux':
                # fp = webdriver.FirefoxProfile(ub_profile)
                # fp.set_preference('network.proxy.type', 1)  # int
                # fp.set_preference('network.proxy.socks', '127.0.0.1')  # string
                # fp.set_preference('network.proxy.socks_port', 9090)  # int
                # fp.set_preference('network.proxy.socks_version', 5)
                options = Options()
                options.headless = True
                self.driver = webdriver.Firefox(options=options) #, firefox_profile=fp)
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

    def close_driver(self):
        self.driver.close