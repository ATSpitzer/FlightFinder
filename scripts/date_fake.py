from Page_Explorer.Trip.TripResults_Explorer import TripResultsExplorer
from ResultParser import combine_result_dicitonary, filter_combined_results
import json
import pandas


URL_1="https://us.trip.com/hotels/list?city=810&countryId=83&checkin=2020/08/19&checkout=2020/08/20&optionId=810&optionType=City&directSearch=1&optionName=Spa&display=Colombo&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1"
URL_2="https://us.trip.com/hotels/list?city=810&countryId=0&checkin=2020/09/20&checkout=2020/09/21&optionId=810&optionType=City&directSearch=1&optionName=Spa&display=Colombo&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1"
URL_3="https://us.trip.com/hotels/list?city=810&countryId=83&checkin=2020/10/23&checkout=2020/10/24&optionId=810&optionType=City&directSearch=1&optionName=Colombo%20Spa&display=Colombo&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1"

# te1 = TripResultsExplorer(start_url=URL_1)
# te2 = TripResultsExplorer(start_url=URL_2)
te3 = TripResultsExplorer(start_url=URL_3)

# r1 = te1.build_results()
# r1_json = json.dumps(r1)
# r2 = te2.build_results()
# r2_json = json.dumps(r2)
# r3 = te3.build_results()
# r3_json = json.dumps(r3)

# with open('res_1.json', 'w') as j1:
#     j1.write(r1_json)
#     j1.close()
#
# with open('res_2.json', 'w') as j2:
#     j2.write(r2_json)
#     j2.close()
#

#
with open('res_1.json','r') as j1:
    r1j = j1.read()

with open('res_2.json','r') as j2:
    r2j = j2.read()

r1 = json.loads(r1j)
r2 = json.loads(r2j)
#
#print(r1)
#print(r1.__class__)
#
#print(r2)
#print(r2.__class__)
#
#print("Adding r1")
end_results = {}
end_results = combine_result_dicitonary(end_results, r1, 'uk')
#print(end_results)

#print("Adding r2")
end_results = combine_result_dicitonary(end_results, r2, 'usa')
#print (end_results)

# #print("Adding r3")
# end_results = combine_result_dicitonary(end_results, r3, 'india')
# #print (end_results)

res_comb = json.dumps(end_results)
with open('res_combined.json','w') as j3:
    j3.write(res_comb)
    j3.close()

filtered_res = filter_combined_results(end_results, 'list-price')
#print(filtered_res)
filt_res = json.dumps(filtered_res)
#print(filt_res)
with open('res_filtered.json','w') as j4:
    j4.write(filt_res)
    j4.close()


table = pandas.read_json(json.dumps(filtered_res), orient='index')
print(str(table))
# print('Search: "Colombo"\tKeywords:"Spa"\tAug 19 2020 to Aug 20 2020')
# print(table)

# te1.close_driver()
# te2.close_driver()
# te3.close_driver()