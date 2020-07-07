from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


import os
import time

class PageExplorer():

    def __init__(self, start_url="http://www.edreams.com", driver_element=None):
        if driver_element:
            print("Existing driver found")
            self.driver = driver_element
        else:
            self.driver = webdriver.Chrome("C:\chromedriver.exe")
            self.driver.maximize_window()
            self.driver.get(start_url)

        #Just wait 1 second since it may take a moment for page to properly load
        time.sleep(1)

        self.service_country = os.getenv('COUNTRY_SERVICE','usa')

        self.initial_page_setup()

    def initial_page_setup(self):
        """
        This is just a sloppy way to find and click the accept cookies button so it doesn't get in the way
        Some extensions will also toake this opportunity to define other buttons somewhere on the page to be called later
        """
        buttons = self.driver.find_elements_by_tag_name('button')
        for b in buttons:
            if b.text == 'Understood':
                b.click()

    def get_driver_object(self):
        return self.driver

    def check_url(self):
        title = self.driver.title
        url = self.driver.current_url
        print("URL: {cur_url}\tTitle: {title}".format(cur_url=url, title=title))

    def close_driver(self):
        self.driver.close()
