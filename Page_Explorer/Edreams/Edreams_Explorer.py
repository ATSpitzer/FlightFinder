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

class EdreamsExplorer(PageExplorer):

    def __init__(self, start_url="http://www.edreams.com", driver_element=None, **kwargs):
        super().__init__(start_url=start_url, driver_element=driver_element, **kwargs)
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
