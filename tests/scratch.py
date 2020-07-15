from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get("http://www.python.org")
# vc.stop_vpn()
# vc.start_vpn()
#
# vc.status_vpn()



# vc = VpnClient()
# vc.status_vpn()


# stopall="systemctl stop shadowsocks-libev-local@*.service"
# pexpect.spawn("/usr/bin/{sa}".format(stopall))


from Page_Explorer.LeakTest.LeakTest_Explorer import LeakTestExplorer
from Vpn_Tool.VpnTool import VpnClient

vc = VpnClient()
vc.stop_vpn('all')
vc.start_vpn('uk')
le = LeakTestExplorer()
le.describe_connection()

print('stopping uk vpn')
vc.stop_vpn('uk')
print('connecting to inda')
vc.start_vpn('india')
print('closing driver')
le.close_driver()
print('New connection')
le = LeakTestExplorer()
# le = LeakTestExplorer(le.driver.refresh())
print('Describing')
le.describe_connection()

# import subprocess
#
# cs="sudo systemctl status shadowsocks-libev-local@ssClientConfig_mumbai"
# cmd = 'sudo /bin/systemctl status {cs}.service'.format(cs=cs)
# completed = subprocess.run( cmd, shell=True, check=True, stdout=subprocess.PIPE )