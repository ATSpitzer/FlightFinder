import unittest
from Page_Explorer.LeakTest.LeakTest_Explorer import LeakTestExplorer
from Vpn_Tool.VpnClient import VpnClient

class MyTestCase(unittest.TestCase):
    COUNTRY_CONV = {
        "usa": "United States",
        # "uk": "United Kingdom",
        "india": "India"
    }
    # vpn_dictionary = {}
    # for country in COUNTRY_CONV:
    #     vpn_dictionary[country] = {}
    #     vpn_dictionary[country]['vpn'] = VpnClient(country)
    #     vpn_dictionary[country]['vpn'].start_vpn()
    #     vpn_dictionary[country]['webdriver'] = LeakTestExplorer(country=country)

    def check_country(self, test_country_short):
        test_ip = self.vpn_dictionary[test_country_short]['vpn'].config_options[test_country_short]['server']
        try:
            test_country_long = self.COUNTRY_CONV[test_country_short]
        except:
            print("Country tested not found in abbreviation dictionary")
            raise

        # le = self.vpn_dictionary[test_country_short]['webdriver']
        le = LeakTestExplorer(test_country_short)
        le.describe_connection()

        found_ip=le.ip_address
        found_country=le.connection_country

        try:
            assert test_ip == found_ip, "Expected dnsleakt to detect ip-address as {ip}, but instead found {fip}}".format(ip=test_ip, fip=found_ip)
            assert test_country_long == found_country, "Expected dnsleak to detect country as {tc}, but instead found {fc}".format(tc=test_country_long, fc=found_country)
        finally:
            le.kill_driver()
            
    # def test_uk(self):
    #     self.check_country('uk')

    def test_india(self):
        self.check_country('india')

    def test_usa(self):
        self.check_country('usa')

if __name__ == '__main__':
    unittest.main()
