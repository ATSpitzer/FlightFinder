from Page_Explorer.Page_Explorer import PageExplorer
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
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.ID, search_bar_id)))

        print("Now looking for buttons")
        # Sometimes, there is before getting to the page we want, there is a loading page. Wait for the loading page to end. This is indicated by the presence of a home page link since there are not clickable links on the loading page
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "button")))
        buttons = self.driver.find_elements_by_tag_name('button')

        for b in buttons:
            if b.text == 'UNDERSTOOD':
                print("Found UNDERSTOOD button. Clicking.")
                b.click()
                break
