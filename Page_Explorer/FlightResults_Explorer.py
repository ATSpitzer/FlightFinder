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
        screen_name = "screen_1.png".format(d=date)
        self.driver.save_screenshot(screen_name)

        search_bar_id="onelinebutton_search_manager"
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.ID, search_bar_id)))
        # sb=self.driver.find_element_by_id(search_bar_id)
        # search_bar_button = sb.find_element_by_tag_name('button')
        # y=0
        # print(sb.__dict__)
        # try:
        #     sb.screenshot('searchbar1.png')
        # except:
        #     pass
        # while((search_bar_button.text is None) or (y<40)):
        #     print("No sb text found - {y} - {t}".format(y=y, t=search_bar_button.text))
        #     time.sleep(1)
        #     y=y+1
        #     search_bar_button = sb.find_element_by_tag_name('button')
        # print("search_bar_button_text: {sbt}".format(sbt=search_bar_button.text))
        # time.sleep(30)
        # sb=self.driver.find_element_by_id(search_bar_id)
        # print(sb.__dict__)
        # try:
        #     sb.screenshot('searchbar2.png')
        # except:
        #     pass

        # date = time.time()
        # print("At {d} found search_bar".format(d=date))
        # screen_name = "screen_2.png".format(d=date)
        # self.driver.save_screenshot(screen_name)

        print("Now looking for buttons")
        # Sometimes, there is before getting to the page we want, there is a loading page. Wait for the loading page to end. This is indicated by the presence of a home page link since there are not clickable links on the loading page
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "button")))
        buttons = self.driver.find_elements_by_tag_name('button')


        x=0
        for b in buttons:
            print("{x}: {t}".format(x=x, t=b.text))
            # b.save_screenshot("button_{x}.png".format(x=x))
            x = x + 1
            if b.text == 'UNDERSTOOD':
                print("Found UNDERSTOOD button. Clicking.")
                b.click()
                break
