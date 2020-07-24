from selenium.common.exceptions import NoSuchElementException, TimeoutException
from Page_Explorer.Page_Explorer import PageExplorer
from Page_Explorer.Trip.locators import HotelSearchLocators as hsl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas
import json
import time

class TripResultsExplorer(PageExplorer):
    SAMPLE_RESULT="https://us.trip.com/hotels/list?city=810&countryId=0&checkin=2020/08/03&checkout=2020/08/04&optionId=810&optionType=City&directSearch=1&optionName=Colombo%20Spa&display=Colombo&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1"
    def __init__(self, start_url="http://us.trip.com", driver_element=None, scroll_to_bottom=False, **kwargs):
        super().__init__(start_url=start_url, driver_element=driver_element, **kwargs)
        # print("Page loaded")
        # self.driver.maximize_window()
        # self.driver.find_element(*hsl.HOTEL_FOOTER).location_once_scrolled_into_view
        # self.driver.save_screenshot('starting_page.png')
        # WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
        #     (By.CLASS_NAME, 'more-hotel-title font-bold')))
        # print("More results found")

        def check_bottom():
            try:
                bottom = self.driver.find_element(*hsl.NO_MORE_RESULTS)
                return bottom.text == "No additional hotels available"
            except NoSuchElementException:
                return False

        # self.driver.implicitly_wait(30)
        bottom = check_bottom()# or scroll_to_bottom
        h_count=0
        while not bottom:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(hsl.MORE_RESULTS_2))
            self.driver.find_element(*hsl.MORE_RESULTS_2).location_once_scrolled_into_view
            WebDriverWait(self.driver, 4).until(EC.invisibility_of_element(hsl.RESULTS_LOADING))
            try:
                self.driver.find_element(*hsl.MORE_RESULTS_BUTTON).click()
                print("Found search more button")
            except:
                pass
            # try:
            #     WebDriverWait(self.driver, 4).until(EC.presence_of_element_located(hsl.MORE_RESULTS_3))
            # except TimeoutException:
            #     bottom = check_bottom()
            bottom = check_bottom()
            hotel_list_page = self.driver.find_element(*hsl.HOTEL_LIST_PAGE)
            self.hotel_list_parent = hotel_list_page.find_element(*hsl.HOTEL_LIST)
            self.hotel_list = self.hotel_list_parent.find_elements(*hsl.HOTEL_CARD)
            if len(self.hotel_list) > h_count:
                h_count = len(self.hotel_list)
                print(h_count)
            else:
                h_count = len(self.hotel_list)

        hotel_list_page = self.driver.find_element(*hsl.HOTEL_LIST_PAGE)
        hotel_list_page.location_once_scrolled_into_view
        self.driver.implicitly_wait(5)
        self.hotel_list_parent = hotel_list_page.find_element(*hsl.HOTEL_LIST)
        self.hotel_list = self.hotel_list_parent.find_elements(*hsl.HOTEL_CARD)

    def try_more_results_button(self):
        print("Looking for more entries")
        buttons = self.driver.find_elements(*hsl.MORE_RESULTS_BUTTON)
        if len(buttons) >= 1:
            time.sleep(1)
            button = buttons[0]
            button.location_once_scrolled_into_view
            time.sleep(1)
            button.click()

    def try_more_results_passive(self):
        print("Checking for more results footer")
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(hsl.MORE_RESULTS_2))
        print("Footer found, pausing for 1 second")
        time.sleep(1)
        self.driver.find_element(*hsl.MORE_RESULTS_2).location_once_scrolled_into_view

    def wait_for_loading(self):
        print("Waiting for there to be no loading")
        WebDriverWait(self.driver, 4).until(EC.invisibility_of_element(hsl.RESULTS_LOADING))
        print("There is no loading, pausing for 1 second")
        time.sleep(1)
        self.driver.find_element(*hsl.MORE_RESULTS_2).location_once_scrolled_into_view

    def print_cards(self):
        """
        Prints out the hotels found in search result. Only for debugging.
        :return:
        """
        cards = self.hotel_list
        i = 0
        for card in cards:
            i = i + 1
            try:
                hc = HotelCard(card)
            except NoSuchElementException:
                print("Exception reading card {i}".format(i=i))
                # card.screenshot('Broken_Card_{i}.png'.fromat(i=i))
                raise
            print("Hotel {i}:\n\t{t}\n\tBefore tax: {p1}\tAfter tax: {p2}".format(i=i, t=hc.title, p1=hc.price_displayed, p2=hc.post_tax))

    def build_results(self):
        """
        Parse the search results for hotels on Trip.com into a dictionary
        :return: Dictionary of hotels and their prices
        """
        results = {}
        duplicates = {}
        dup_count = 0
        self.hotel_list_parent.screenshot('hotel_list.png')
        for card in self.hotel_list:
            try:
                card_local = card.location_once_scrolled_into_view
                hc = HotelCard(card)
                entry = hc.get_price_dictionary()
                if entry['title'] in results.keys():
                    duplicates[dup_count] = {entry['title']:entry['result'],'location':card_local}
                    card.screenshot("screenshots/{title}_{c}.png".format(title=entry['title'], c=dup_count))
                    dup_count = dup_count + 1
                else:
                    results[entry['title']] = entry['result']
                    # try:
                    #     if float(entry['result']['real-price'].replace('$','').replace(',','')) > 1000:
                    #         print("OOPS")
                    #         # print('{t}:\t {p}'.format(p=float(entry['result']['real-price'].replace('$','').replace(',',''),t=entry['title']))
                    #         # card.screenshot("screenshots/{title}.png".format(title=entry['title']))
                    # except:
                    #     print("ex hit")
                    #     pass
                    #     # print(entry)
                    print(". . . . . . . . . . . . . . . . . . . . . . . . . . ")
                    print('{t}:\t {p}'.format(p=entry['result']['real-price'].replace('$', ''), t=entry['title']))
                    print("{t}\n\tBefore tax: {p1}\tAfter tax: {p2}".format(t=hc.title,
                                                                                          p1=hc.price_displayed,
                                                                                          p2=hc.post_tax))

                    # entry = hc.get_price_dictionary()
                    results[entry['title']] = entry['result']
            except NoSuchElementException:
                print("Exception reading card. Probably no price")
                if len(card.find_elements(*hsl.HOTEL_MEMBER)) >= 1:
                    print("'Member' found, skipping")
                elif len(card.find_elements(*hsl.HOTEL_SOLD_OUT)) >=1:
                    print("Hotel Sold out")
                else:
                    raise
        # print(pandas.read_json(json.dumps(duplicates), orient='index'))
        return results

class HotelCard(object):
    def __init__(self, card):
        card.location_once_scrolled_into_view
        self.title = card.find_element(*hsl.HOTEL_TITLE).text
        price_section = card.find_element(*hsl.HOTEL_PRICE_SECTION)
        self.post_tax = price_section.find_element(*hsl.HOTEL_TAX_SECTION).text.replace('After tax ','')
        self.price_pretax = card.find_element(*hsl.HOTEL_PRETAX)
        self.price_displayed = self.price_pretax.text
        promos = price_section.text.splitlines()
        try:
            self.promos_trimmed = promos[1 + promos.index(price_section.find_element(*hsl.HOTEL_TAX_SECTION).text):promos.index('Select')]
        except ValueError:
            print("Expected word missing from text for - {t}".format(t=self.title))
            print(promos)
            if len(promos) > 3:
                self.promos_trimmed = promos[2:-1]
            else:
                self.promos_trimmed = []

    def get_price_dictionary(self):
        return \
            {
                'title': self.title,
                'result':{
                        'list-price':self.price_displayed,
                        'real-price':self.post_tax,
                        'promos':self.promos_trimmed
                    }

            }
