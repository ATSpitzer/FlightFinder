from Page_Explorer.Trip.TripResults_Explorer import TripResultsExplorer
from Page_Explorer.Trip.locators import HotelSearchLocators as hsl
from ResultParser import combine_result_dicitonary, filter_combined_results
import json
import pandas

pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)


URL_1="https://us.trip.com/hotels/list?city=7291&countryId=108&checkin=2021/02/17&checkout=2021/02/18&optionId=7291&optionType=IntlCity&display=Labuan%20Bajo&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=0"
# https://us.trip.com/hotels/list?city=3789&countryId=66&checkin=2020/10/22&checkout=2020/10/23&optionId=3789&optionType=IntlCity&directSearch=0&display=Hawaii-Maui&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=0"
URL_2="https://us.trip.com/hotels/list?city=3789&countryId=66&checkin=2021/03/08&checkout=2021/03/09&optionId=3789&optionType=IntlCity&directSearch=0&display=Hawaii-Maui&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=0"
URL_3="https://us.trip.com/hotels/list?city=3789&countryId=66&checkin=2021/01/08&checkout=2021/01/09&optionId=3789&optionType=IntlCity&directSearch=0&display=Hawaii-Maui&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=0"


def perform_search(num, URL):
    te = TripResultsExplorer(start_url=URL)
    te.driver.maximize_window()
    c = 100
    for h in te.hotel_list:
        print("{c}:  {t}".format(c=c,t=h.find_element(*hsl.HOTEL_TITLE).text))
        c = c + 1
    r = te.build_results()
    print(json.dumps(te.driver.get_cookies()))
    r_j = json.dumps(r)
    print(pandas.read_json(r_j, orient='index'))
    with open('res_{n}.json'.format(n=num), 'w') as j:
        j.write(r_j)
    return r

r1 = perform_search(1, URL_1)
# r2 = perform_search(2, URL_2)
# r3 = perform_search(3, URL_3)
#
# #print("Adding r1")
# end_results = {}
# end_results = combine_result_dicitonary(end_results, r1, 'uk')
# #print(end_results)
#
# #print("Adding r2")
# end_results = combine_result_dicitonary(end_results, r2, 'usa')
# #print (end_results)
#
# #print("Adding r3")
# end_results = combine_result_dicitonary(end_results, r3, 'india')
# #print (end_results)
#
# res_comb = json.dumps(end_results)
# with open('res_combined.json','w') as j3:
#     j3.write(res_comb)
#     j3.close()
#
# filtered_res = filter_combined_results(end_results, 'list-price')
# #print(filtered_res)
# filt_res = json.dumps(filtered_res)
# #print(filt_res)
# with open('res_filtered.json','w') as j4:
#     j4.write(filt_res)
#     j4.close()
#
#
# table = pandas.read_json(json.dumps(filtered_res), orient='index')
# print(str(table))
# print('Search: "Colombo"\tKeywords:"Spa"\tAug 19 2020 to Aug 20 2020')
# print(table)

# te1.close_driver()
# te2.close_driver()
# te3.close_driver()