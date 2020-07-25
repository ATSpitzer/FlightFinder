from Page_Explorer.Trip.TripResults_Explorer import TripResultsExplorer
from ResultParser import combine_result_dicitonary, filter_combined_results
import json
import pandas

pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)


URL_1="https://us.trip.com/hotels/list?city=7291&countryId=108&checkin=2021/02/17&checkout=2021/02/18&optionId=7291&optionType=IntlCity&display=Labuan%20Bajo&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=0"


def perform_search(URL, country):
    te = TripResultsExplorer(start_url=URL, country=country)
    # te.driver.maximize_window()
    r = te.build_results()
    print(json.dumps(te.driver.get_cookies()))
    r_j = json.dumps(r)
    # print(pandas.read_json(r_j, orient='index'))
    with open('res_{n}.json'.format(n=country), 'w') as j:
        j.write(r_j)
    return r

# usa = perform_search(url = URL_1, country='usa')
india = perform_search(url= URL_1, country='inda')

end_results = {}
# end_results = combine_result_dicitonary(end_results, usa, 'usa')
end_results = combine_result_dicitonary(end_results, india, 'india')
res_comb = json.dumps(end_results)
with open('res_combined.json','w') as j3:
    j3.write(res_comb)
    j3.close()
#
filtered_res = filter_combined_results(end_results, 'list-price')
filt_res = json.dumps(filtered_res)
with open('res_filtered.json','w') as j4:
    j4.write(filt_res)
    j4.close()
#
#
table = pandas.read_json(json.dumps(filtered_res), orient='index')
