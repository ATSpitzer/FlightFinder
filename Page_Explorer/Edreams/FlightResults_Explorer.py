from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

from Page_Explorer.Edreams.Edreams_Explorer import PageExplorer
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class FlightResults(PageExplorer):

    def initial_page_setup(self):
        time.sleep(3)
        date = time.time()
        print("At {d} looking for search_bar".format(d=date))
        # screen_name = "screen_1.png".format(d=date)
        # self.driver.save_screenshot(screen_name)

        search_bar_id="onelinebutton_search_manager"
        try:
            WebDriverWait(self.driver, 45).until(
                EC.element_to_be_clickable(
                    (By.ID, search_bar_id)))
        except TimeoutException:
            print("Timeout while looking for searchbar")
            self.driver.save_screenshot("timeouterror_{cntry}.png".format(cntry=self.service_country))
            raise


        print("Now looking for buttons")
        # We want to wait fo the page to load then iterate through the buttons found
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "button")))
        buttons = self.driver.find_elements_by_tag_name('button')

        for b in buttons:
            if b.text == 'UNDERSTOOD':
                print("Found UNDERSTOOD button. Clicking.")
                try:
                    b.click()
                except ElementClickInterceptedException:
                    print("Timeout while looking for searchbar")
                    self.driver.save_screenshot("sessionexpire_{cntry}.png".format(cntry=self.service_country))
                    self.driver.find_element_by_id("sessionAboutToExpireAlert").click()
                    b.click()
                break

        # selenium.common.exceptions.ElementClickInterceptedException: Message: Element < buttonclass ="odf-btn odf-btn-sm odf-space-outer-right-m odf-btn-primary ack_button" >
        # is not clickable at point (140, 597) because another element
        # < div id="sessionAboutToExpireAlert" class ="od-z-index-9999 ui_dialog_box ui_dialog_content odf-lightbox-bg open opened" >
        # obscures it

