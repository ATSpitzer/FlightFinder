from selenium.webdriver.common.by import By


class HotelSearchLocators():
    """locators on the results page when searching for hotels"""
    HOTEL_LIST_PAGE = (By.CLASS_NAME, 'hotel-list-page')
    HOTEL_LIST = (By.XPATH, '//ul[@class="long-list"]')

    #Hotel Card marked by class named "with-decorator-wrap
    HOTEL_CARD = (By.XPATH, './/li/div[@class="with-decorator-wrap"]')
    #Hotel title on left part, some way down in span with class named "name font-bold"
    HOTEL_TITLE = (By.CLASS_NAME, "list-card-title") #By.XPATH, '//span[@class="name font-bold"]')

    #div class='list-card-price' contains many price related values
    HOTEL_PRICE_SECTION = (By.CLASS_NAME, 'list-card-price')
    HOTEL_TAX_SECTION = (By.CLASS_NAME, 'tax')

    #pretax
    HOTEL_PRETAX = (By.XPATH, './/p[@class="price"]/span/div[1]')

    HOTEL_SELECT = (By.CLASS_NAME, "select font-bold")

    #Hotels with member element do not list price and should be skipped over
    HOTEL_MEMBER = (By.CLASS_NAME, "list-card-member")

    #Text before more hotels that don't exactly match search
    MORE_HOTELS = (By.CLASS_NAME, "more-hotel-title font-bold")

    #Scroll for more results
    MORE_RESULTS = (By.CLASS_NAME, 'none-ref')
    MORE_RESULTS_2 = (By.CLASS_NAME, 'list-crumb')
    MORE_RESULTS_3 = (By.CLASS_NAME, 'list-btn-more')

    #Temporarily exists while more results are loading
    RESULTS_LOADING = (By.CLASS_NAME, 'loading')

    # Has text: No additional hotels available
    NO_MORE_RESULTS = (By.CLASS_NAME, 'nothing')
