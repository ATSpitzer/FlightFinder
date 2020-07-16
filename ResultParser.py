def combine_result_dicitonary(existing_results, new_results, search_var):
    for hotel in new_results.keys():
        try:
            existing_results[hotel][search_var]=new_results[hotel]
        except KeyError:
            existing_results[hotel] = {}
            existing_results[hotel][search_var] = new_results[hotel]

    return existing_results

def filter_combined_results(combined_results, filter):
    filtered_results = {}
    for hotel in combined_results.keys():
        filtered_results[hotel] = {}
        for search_var in combined_results[hotel].keys():
            # print(". . . . . . . . . . . . . . . . . . . . . . . . . .")
            # print(hotel + "\t" + search_var)
            # print(combined_results[hotel][search_var])
            # print(combined_results[search_var])
            filtered_results[hotel][search_var] = combined_results[hotel][search_var][filter]
    return filtered_results

