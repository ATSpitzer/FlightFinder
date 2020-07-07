from Page_Explorer.Page_Explorer import PageExplorer
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class FlightResults(PageExplorer):

    def initial_page_setup(self):
        date = time.time()
        print("At {d} looking for buttons".format(d=date))
        # screen_name = "screen_at_{d}.png".format(d=date)
        # self.driver.implicitly_wait(20)
        time.sleep(20)
        # Sometimes, there is before getting to the page we want, there is a loading page. Wait for the loading page to end. This is indicated by the presence of a home page link since there are not clickable links on the loading page
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "button")))
        buttons = self.driver.find_elements_by_tag_name('button')

        date = time.time()
        print("At {d} found buttons".format(d=date))
        # screen_name = "screen_at_{d}.png".format(d=date)
        # self.driver.save_screenshot(screen_name)

        # buttons = self.driver.find_elements_by_tag_name('button')
        print("Buttons found:\n\t{b}".format(b=buttons))
        x=0
        for b in buttons:
            # print("{x}: {t}".format(x=x, t=b.tag_name))
            # b.save_screenshot("button_{x}.png".format(x=x))
            x = x + 1
            if b.text == 'UNDERSTOOD':
                print("Found UNDERSTOOD button. Clicking.")
                b.click()

        date = time.time()
        screen_name = "screen_at_{d}.png".format(d=date)
        self.driver.save_screenshot(screen_name)