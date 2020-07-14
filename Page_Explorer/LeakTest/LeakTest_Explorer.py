from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Page_Explorer.Page_Explorer import PageExplorer
from selenium.webdriver.firefox.options import Options
import platform
import os
import time
from datetime import date

class LeakTestExplorer(PageExplorer):

    def __init__(self, start_url="http://www.dnsleaktest.com", driver_element=None):
        super().__init__(start_url=start_url, driver_element=driver_element)

        self.site_content=self.driver.find_element_by_class_name("welcome")
        # self.site_content.screenshot('s_c.png')

    def describe_connection(self):
        sub_elements = self.site_content.find_elements_by_tag_name('p')
        for s_e in sub_elements:
            text_list = s_e.text.split(' ')
            if text_list[0] == "Hello":
                self.ip_address = text_list[-1]
            elif text_list[0] == "from":
                self.connection_country = s_e.text.split(',')[-1].lstrip()
        print("ip_address: {ip}".format(ip=self.ip_address))
        print("country: {cntry}".format(cntry=self.connection_country))

    def screenshot_connection_info(self, screenshot_name):
        ss_full = "{name}.png".format(name=screenshot_name)
        print("Saving screenshot at {ss_full_path}".format(ss_full_path=ss_full))
        self.site_content.screenshot(ss_full)
