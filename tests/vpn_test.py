import unittest
from Page_Explorer.LeakTest.LeakTest_Explorer import LeakTestExplorer
from Vpn_Tool.VpnClient import VpnClient

class MyTestCase(unittest.TestCase):
    COUNTRY_CONV = {
        "usa": "United States",
        "uk": "United Kingdom",
        "india": "India"
    }

    def setUp(self):
        self.vpn_cli = VpnClient()

    def check_country(self, test_country_short):
        test_ip = self.vpn_cli.config_options[test_country_short]['server']
        try:
            test_country_long = self.COUNTRY_CONV[test_country_short]
        except:
            print("Country tested not found in abbreviation dictionary")
            raise

        print("Stopping vpn")
        self.vpn_cli.stop_vpn()

        print("Starting vpn at {tcs}".format(tcs=test_country_short))
        self.vpn_cli.start_vpn(test_country_short)

        print("Checking vpn")
        self.vpn_cli.status_vpn()

        self.le = LeakTestExplorer()
        self.le.screenshot_connection_info(test_country_short)
        self.le.describe_connection()

        found_ip=self.le.ip_address
        found_country=self.le.connection_country

        try:
            assert test_ip == found_ip, "Expected dnsleakt to detect ip-address as {ip}, but instead found {fip}}".format(ip=test_ip, fip=found_ip)
            assert test_country_long == found_country, "Expected dnsleak to detect country as {tc}, but instead found {fc}".format(tc=test_country_long, fc=found_country)
        finally:
            self.le.close_driver()
            
    def test_uk(self):
        self.check_country('uk')

    def test_india(self):
        self.check_country('india')

    def test_usa(self):
        self.check_country('usa')

if __name__ == '__main__':
    unittest.main()
