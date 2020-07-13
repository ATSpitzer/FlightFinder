import string
import unittest
import random

from Page_Explorer.LeakTest.LeakTest_Explorer import LeakTestExplorer
from Vpn_Tool.VpnTool import VpnClient




class MyTestCase(unittest.TestCase):
    COUNTRY_CONV = {
        "usa": "United States",
        "uk": "United Kingdom",
        "india": "India"
    }

    def setUp(self):
        self.vpn_cli = VpnClient()
        self.le = LeakTestExplorer()
        self.test_screenshot_dir=''.join(random.choices(string.ascii_uppercase, k=5))


    def check_country(self, test_country_short):
        test_ip = self.vpn_cli.config_options[test_country_short]['server']
        try:
            test_country_long = self.COUNTRY_CONV[test_country_short]
        except:
            print("Country tested not found in abbreviation dictionary")
            raise

        self.vpn_cli.stop_vpn()
        self.vpn_cli.start_vpn(test_country_short)
        self.le.driver.refresh()
        self.le.screenshot_connection_info(screenshot_dir=self.test_screenshot_dir, screenshot_name="{cntry_test}".format(cntry_test=test_country_short))
        self.le.describe_connection()

        assert test_ip == self.le.ip_address, "Expected dnsleakt to detect ip-address as {ip}, but instead found {fip}}".format(ip=test_ip, fip=self.le.ip_address)
        assert test_country_long == self.le.connection_country, "Expected dnsleak to detect country as {tc}, but instead found {fc}".format(tc=test_country_long, fc=self.le.connection_country)

    def test_uk(self):
        self.check_country('uk')

    def test_india(self):
        self.check_country('india')

        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
