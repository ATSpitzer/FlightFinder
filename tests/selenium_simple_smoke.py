import unittest
import platform
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class MyTestCase(unittest.TestCase):
    """
    This is just a really simple test to make sure that selenium can run and connect to the internet. Does not run with proxy
    """
    def setUp(self):
        if platform.system() == 'Windows':
            options = webdriver.ChromeOptions()
            # options.add_argument
            options.add_experimental_option("detach", True)
            self.driver = webdriver.Chrome("C:\chromedriver.exe", options=options)
        elif platform.system() == 'Linux':
            # Using Firefox Connection
            options = webdriver.firefox.options.Options()
            options.headless = True
            self.driver = webdriver.Firefox(options=options)
    def tearDown(self):
        super().tearDown()
        self.driver.quit()

    def test_python_page(self):
        print("Loading 'http://www.python.org'")
        self.driver.get("http://www.python.org")
        print("Page loaded")
        print("Title: {t}".format(t=self.driver.title))
        assert "Python" in self.driver.title, 'Expected to find "Python" in title'

if __name__ == '__main__':
    unittest.main()
