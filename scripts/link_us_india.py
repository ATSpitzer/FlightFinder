from Vpn_Tool.VpnClient import VpnClient
from Page_Explorer.Trip.TripResults_Explorer import TripResultsExplorer
from ResultParser import combine_result_dicitonary, filter_combined_results
import json
import pandas

URL_1="https://us.trip.com/hotels/list?city=810&countryId=83&checkin=2020/08/19&checkout=2020/08/20&optionId=810&optionType=City&directSearch=1&optionName=Spa&display=Colombo&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1"

def perform_search(url=URL_1):
    te = TripResultsExplorer(start_url=url)
    results = te.build_results()
    te.close_driver()
    te.driver.quit()
    return results

vc = VpnClient()
vc.stop_vpn('all')

#USA
vc.start_vpn('usa')
usa = perform_search()
vc.stop_vpn('usa')

#India
vc.start_vpn('india')
india = perform_search()
vc.stop_vpn('india')

end_results = {}
end_results = combine_result_dicitonary(end_results, usa, 'usa')
end_results = combine_result_dicitonary(end_results, india, 'india')
filtered_res = filter_combined_results(end_results, 'real-price')

table = pandas.read_json(json.dumps(filtered_res), orient='index')
with open('search_results_colombo.txt','w') as sr:
    sr.write("Link: {url}\n\nResults:\n---------------------------------\n{res}".format(url=URL_1,res=str(table)))
print("Link: {url}\n\nResults:\n---------------------------------\n{res}".format(url=URL_1,res=str(table)))
