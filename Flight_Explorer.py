from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


import os
import time

# start_url="http://www.edreams.com"
# driver = webdriver.Chrome("C:\chromedriver.exe")
# print(driver.__class__)
# driver.get(start_url)
class FlightFinder():

    def __init__(self, start_url="http://www.edreams.in"):
        self.driver = webdriver.Chrome("C:\chromedriver.exe")
        self.driver.maximize_window()
        time.sleep(2)

        self.driver.get(start_url)

        buttons = self.driver.find_elements_by_tag_name('button')
        for b in buttons:
            if b.text == 'Understood':
                b.click()
            if b.text == 'Search Flights':
                self.search_button = b


        self.service_country = os.getenv('COUNTRY_SERVICE','usa')
        self.price=None
        self.currency=None
        self.flight_list={}

    def check_url(self):
        title = self.driver.title
        url = self.driver.current_url
        print("URL: {cur_url}\tTitle: {title}".format(cur_url=url, title=title))

    def close_driver(self):
        self.driver.close()

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

        airport_string = "{end} -".format(end=end)
        dd_list=to_value.find_elements_by_tag_name('li')
        print(dd_list)
        for el in dd_list:
            print(el.text)
            # if el.text == airport_string:
            #     el.click()
            #     break

    def set_day(self, day):
        month = self.driver.find_element_by_class_name('odf-calendar-month')
        days = month.find_elements_by_class_name('odf-calendar-day')
        print(days)
        for d in days:
            print(d.text)
            if d.text == day:
                d.click()
                break



    # odf-btn odf-btn-secondary odf-btn-circle odf-btn-circle-md
    def select_month(self, month, year):
        calendar = self.driver.find_element_by_class_name("odf-calendar-title")
        cal_string = "{m} '{y}".format(m=month, y=year)
        next_month = self.driver.find_element_by_xpath("//span[@glyph='arrow-right']")
        while(calendar.text != cal_string):
            next_month.click()
            calendar = self.driver.find_elements_by_class_name("odf-calendar-title")[0]




ff = FlightFinder()
# ff.check_url()
ff.search_flight_rt(start='CGK',end='LOP',date1="July 19 20",date2="July 25 20")