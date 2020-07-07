from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Page_Explorer.Page_Explorer import PageExplorer
import os
import time

class FlightSearch(PageExplorer):

    def initial_page_setup(self):
        buttons = self.driver.find_elements_by_tag_name('button')
        for b in buttons:
            if b.text == 'Understood':
                # print("Found understood button, clicking")
                # print(b.text)
                b.click()
            if b.text == 'Search Flights':
                self.search_button = b

    def check_url(self):
        title = self.driver.title
        url = self.driver.current_url
        print("URL: {cur_url}\tTitle: {title}".format(cur_url=url, title=title))

    def search_flight_rt(self, start, end, date1, date2):
        self.set_depart_place(start)
        self.driver.implicitly_wait(3)
        self.set_destination_place(end)
        self.driver.implicitly_wait(3)

        self.driver.find_element_by_xpath("//input[@placeholder='Departure']").click()
        dept_date = date1.split(' ')
        ret_date = date2.split(' ')

        self.select_month(dept_date[0], dept_date[2])
        self.set_day(dept_date[1])

        self.driver.find_element_by_xpath("//input[@placeholder='Return']").click()
        self.select_month(ret_date[0], ret_date[2])
        self.set_day(ret_date[1])

        self.search_button.click()

    def set_depart_place(self, start):
        from_value = self.driver.find_element_by_xpath("//input[@placeholder='From']")
        from_value.send_keys(start)

    def set_destination_place(self, end):
        to_value = self.driver.find_element_by_xpath("//input[@placeholder='To']")
        to_value.send_keys(end)
        time.sleep(2)
        dd_list = to_value.parent.find_element_by_tag_name('ul')\
            .find_elements_by_tag_name('li')
        # print(dd_list)
        #

    def set_day(self, day):
        month = self.driver.find_element_by_class_name('odf-calendar-month')
        days = month.find_elements_by_class_name('odf-calendar-day')
        for d in days:
            if d.text == day:
                d.click()
                break

    def select_month(self, month, year):
        calendar = self.driver.find_element_by_class_name("odf-calendar-title")
        cal_string = "{m} '{y}".format(m=month, y=year)
        next_month = self.driver.find_element_by_xpath("//span[@glyph='arrow-right']")
        while(calendar.text != cal_string):
            next_month.click()
            calendar = self.driver.find_elements_by_class_name("odf-calendar-title")[0]
