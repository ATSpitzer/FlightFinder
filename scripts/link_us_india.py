from Vpn_Tool.VpnClient import VpnClient
from Page_Explorer.Trip.TripResults_Explorer import TripResultsExplorer
from ResultParser import combine_result_dicitonary, filter_combined_results
import sys
import json
import pandas
import random

if len(sys.argv) <= 1:
    URL_1="https://us.trip.com/hotels/list?city=810&countryId=83&checkin=2020/08/19&checkout=2020/08/20&optionId=810&optionType=City&directSearch=1&optionName=Spa&display=Colombo&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1"
else:
    URL_1=sys.argv[1]
def perform_search(country, url=URL_1):
    te = TripResultsExplorer(start_url=url, country=country)
    results = te.build_results()
    te.kill_driver()
    return results

usa = perform_search('usa')
india = perform_search('india')

end_results = {}
end_results = combine_result_dicitonary(end_results, usa, 'usa')
end_results = combine_result_dicitonary(end_results, india, 'india')
filtered_res = filter_combined_results(end_results, 'real-price')

table = pandas.read_json(json.dumps(filtered_res), orient='index')
r = random.randrange(500)
filename = 'search_results_{r}.txt'.format(r=r)
print("Saving result as {fn}".format(fn=filename))
with open(filename,'w') as sr:
    sr.write("Link: {url}\n\nResults:\n---------------------------------\n{res}".format(url=URL_1,res=str(table)))
print("Link: {url}\n\nResults:\n---------------------------------\n{res}".format(url=URL_1,res=str(table)))
