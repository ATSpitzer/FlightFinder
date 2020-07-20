from selenium.common.exceptions import NoSuchElementException
from Page_Explorer.Page_Explorer import PageExplorer
from Page_Explorer.Trip.locators import HotelSearchLocators as hsl

class TripResultsExplorer(PageExplorer):
    SAMPLE_RESULT="https://us.trip.com/hotels/list?city=810&countryId=0&checkin=2020/08/03&checkout=2020/08/04&optionId=810&optionType=City&directSearch=1&optionName=Colombo%20Spa&display=Colombo&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1"
    def __init__(self, start_url="http://us.trip.com", driver_element=None, **kwargs):
        super().__init__(start_url=start_url, driver_element=driver_element, **kwargs)
        hotel_list_page = self.driver.find_element(*hsl.HOTEL_LIST_PAGE)
        self.hotel_list_parent = hotel_list_page.find_element(*hsl.HOTEL_LIST)
        self.hotel_list = self.hotel_list_parent.find_elements(*hsl.HOTEL_CARD)

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
        self.hotel_list_parent.screenshot('hotel_list.png')
        for card in self.hotel_list:
            try:
                hc = HotelCard(card)
                entry = hc.get_price_dictionary()
                results[entry['title']] = entry['result']
            except NoSuchElementException:
                print("Exception reading card. Checking for 'Member'")
                if card.find_element(*hsl.HOTEL_MEMBER):
                    print("'Member' found, skipping")
                else:
                    print("'Member' not found")
                    raise
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
