from Vpn_Tool.VpnClient import VpnClient
from Page_Explorer.Trip.TripResults_Explorer import TripResultsExplorer
from ResultParser import combine_result_dicitonary, filter_combined_results
import sys
import json
import pandas
import random
if len(sys.argv) <= 1:
    URL_1="https://us.trip.com/hotels/list?city=3789&countryId=66&checkin=2021/02/08&checkout=2021/02/09&optionId=3789&optionType=IntlCity&directSearch=0&display=Hawaii-Maui&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=0&highPrice=3000&barCurr=USD&bookable=&sort=AppointRank&showtotalamt=1&lowPrice=10"
else:
    URL_1=sys.argv[1]
def perform_search(country, url=URL_1):
    te = TripResultsExplorer(start_url=url, country=country)
    results = te.build_results()
    loaded_url = te.check_url()
    te.kill_driver()
    return results, loaded_url
usa, usa_url = perform_search('usa')
india, india_url = perform_search('india')
end_results = {}
end_results = combine_result_dicitonary(end_results, usa, 'usa')
end_results = combine_result_dicitonary(end_results, india, 'india')
filtered_res = filter_combined_results(end_results, 'real-price')
filtered_res_list = filter_combined_results(end_results, 'list-price')
table_1 = pandas.read_json(json.dumps(filtered_res), orient='index')
table_2 = pandas.read_json(json.dumps(filtered_res_list), orient='index')
table_3 = pandas.read_json(json.dumps(filter_combined_results(end_results, 'promos')),orient='index')
print(str(table_3))
r = random.randrange(500)
filename = 'search_results_{r}.txt'.format(r=r)
print("Loaded urls:")
print("usa:   \t{u}".format(u=usa_url))
print("india: \t{u}".format(u=india_url))
print("Saving result as {fn}".format(fn=filename))
with open(filename,'w') as sr:
    sr.write("Link: {url}\n\nResults:\n---------------------------------\n\nReal Price\n{res}\n\nList Price\n{res2}".format(url=URL_1,res=str(table_1), res2=str(table_2)))
print("\nReal Price\nResults:\n---------------------------------\n{res}".format(res=str(table_1)))
print("\n\nList Price\nResults:\n---------------------------------\n{res}".format(res=str(table_2)))
