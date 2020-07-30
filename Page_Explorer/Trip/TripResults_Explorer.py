from selenium.common.exceptions import NoSuchElementException, TimeoutException
from Page_Explorer.Page_Explorer import PageExplorer
from Page_Explorer.Trip.locators import HotelSearchLocators as hsl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



class TripResultsExplorer(PageExplorer):
    SAMPLE_RESULT="https://us.trip.com/hotels/list?city=810&countryId=0&checkin=2020/08/03&checkout=2020/08/04&optionId=810&optionType=City&directSearch=1&optionName=Colombo%20Spa&display=Colombo&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1"
    def __init__(self, start_url="http://us.trip.com", driver_element=None, scroll_to_bottom=False, **kwargs):
        super().__init__(start_url=start_url, driver_element=driver_element, **kwargs)
        def check_bottom():
            try:
                bottom = self.driver.find_element(*hsl.NO_MORE_RESULTS)
                return bottom.text == "No additional hotels available"
            except NoSuchElementException:
                return False

        # time.sleep(30)
        if scroll_to_bottom:
            bottom = check_bottom()
        else:
            bottom = False

        while not bottom:
            print("Sleep for 5 seconds")
            time.sleep(5)
            print("Check for more results")
            self.try_more_results_button()
            bottom = check_bottom()

        hotel_list_page = self.driver.find_element(*hsl.HOTEL_LIST_PAGE)
        self.hotel_list_parent = hotel_list_page.find_element(*hsl.HOTEL_LIST)
        self.hotel_list = self.hotel_list_parent.find_elements(*hsl.HOTEL_CARD)

        hotel_list_page = self.driver.find_element(*hsl.HOTEL_LIST_PAGE)
        hotel_list_page.location_once_scrolled_into_view
        self.hotel_list_parent = hotel_list_page.find_element(*hsl.HOTEL_LIST)
        self.hotel_list = self.hotel_list_parent.find_elements(*hsl.HOTEL_CARD)

    def try_more_results_button(self):
        print("Looking for more entries - pause for 2 seconds")
        time.sleep(2)
        buttons = self.driver.find_elements(*hsl.MORE_RESULTS_BUTTON)
        if len(buttons) >= 1:
            print("Load more results button found")
            button = buttons[0]
            button.location_once_scrolled_into_view
            button.click()
            self.wait_for_loading()
        else:
            self.try_more_results_passive()

    def try_more_results_passive(self):
        print("Checking for more results footer")
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(hsl.MORE_RESULTS_2))
        print("Footer found, pausing for 5 second")
        time.sleep(5)
        self.driver.find_element(*hsl.MORE_RESULTS_2).location_once_scrolled_into_view
        self.wait_for_loading()

    def wait_for_loading(self):
        print("Looking for loading screen")
        if len(self.driver.find_elements(*hsl.RESULTS_LOADING)) >= 1:
            print("Loading screen found")
            print("Waiting for there to be no loading")
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element(hsl.RESULTS_LOADING))
        print("There is no loading, pausing for 2 second")
        time.sleep(2)
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
            card_local = card.location_once_scrolled_into_view
            hc = HotelCard(card)
            entry = hc.get_price_dictionary()
            if entry['title'] in results.keys():
                duplicates[dup_count] = {entry['title']:entry['result'],'location':card_local}
                dup_count = dup_count + 1
            else:
                results[entry['title']] = entry['result']
        return results

class HotelCard(object):
    def __init__(self, card):
        try:
            self.promos_trimmed = []
            card.location_once_scrolled_into_view
            self.title = card.find_element(*hsl.HOTEL_TITLE).text
            price_section = card.find_element(*hsl.HOTEL_PRICE_SECTION)
            promos = price_section.text.splitlines()
            self.post_tax = price_section.find_element(*hsl.HOTEL_TAX_SECTION).text.replace('After tax ', '')
            self.price_unit = self.post_tax[0]
            self.price_pretax = card.find_element(*hsl.HOTEL_PRETAX)
            self.price_displayed = self.price_pretax.text
            try:
                self.promos_trimmed = promos[1 + promos.index(price_section.find_element(*hsl.HOTEL_TAX_SECTION).text):promos.index('Select')]
            except ValueError:
                print("Expected word missing from text for - {t}".format(t=self.title))
                print(promos)
                if len(promos) > 3:
                    self.promos_trimmed = promos[2:-1]
        except (NoSuchElementException, IndexError):
            print("Exception reading card. Probably no price")
            self.price_unit = None
            self.price_pretax = None
            self.price_displayed = None
            self.post_tax = None
            if len(card.find_elements(*hsl.HOTEL_MEMBER)) >= 1:
                print("'Member' found, skipping")
                self.promos_trimmed.append("Member-price")
            elif len(card.find_elements(*hsl.HOTEL_SOLD_OUT)) >= 1:
                print("Hotel Sold out")
                self.promos_trimmed.append("Sold-out")
            else:
                raise

    def get_price_dictionary(self):
        return \
            {
                'title': self.title,
                'result':{
                        'list-price':self.price_displayed,
                        'real-price':self.post_tax,
                        'promos':self.promos_trimmed,
                        'currency':self.price_unit
                    }

            }
