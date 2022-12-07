import json
import requests
import numpy as np

print("\nIgnore those stupid warnings^^\n")

api_base = "https://covid-api.mmediagroup.fr/v1"

countries = ["US", "Russia", "Brazil"]

for country in countries:
    # DEFINE DICIONARY TO DUMP JSON LATER
    country_dict = {}
    country_dict["country"] = country
    print("Covid confirmed cases statistics")
    print("Country name:", country)
    
    # GET JSON FROM API
    url = api_base + "/history?country=" + country + "&status=confirmed"
    # print(url)
    req = requests.get(url)
    dictionary = json.loads(req.text)

    # DEFINE KEYS, END DATE, LISTS
    key1 = "All"
    key2 = "dates"
    end_date = "2021-12-31"
    cases_lst = []
    date_lst = []

    # APPEND JSON DATA TO LISTS
    for date in dictionary[key1][key2]:
        if date > end_date:
            pass
        else:
            cases_lst.append(dictionary[key1][key2][date])
            date_lst.append(date)
    
    # REVERSE LISTS SO EARLIEST DATES COME FIRST
    cases_lst.reverse()
    date_lst.reverse()

    # CALCULATE DAILY NEW CASES AND APPEND TO LIST
    new_cases = []
    for i in range(1, len(cases_lst)):
        daily_new_cases = cases_lst[i] - cases_lst[i-1]
        new_cases.append(daily_new_cases)

    # GET AVERAGE NUMBER OF NEW DAILY CONFIMED CASES
    avg_new_daily = np.average(new_cases)
    country_dict["avg_new_daily"] = avg_new_daily
    print("Average number of new daily confirmed cases for the entire dataset:", avg_new_daily)

    # GET HIGHEST NUMBER OF NEW CASES IN A DAY
    highest_num = max(new_cases)
    # print("highest_num", highest_num)
    index = new_cases.index(highest_num)
    # print("index", index)
    date = date_lst[index]
    country_dict["highest_new_cases"] = date
    print("Date with the highest new number of confirmed cases: %s with %d new cases" % (date, highest_num))

    # MOST RECENT DATE WITH NO NEW CASES
    for i in range((len(new_cases) - 1), 0, -1):
        if new_cases[i] == 0:
            date = date_lst[i]
            break
    country_dict["recent_no_new_cases"] = date
    print("Most recent date with no new cases:", date)

    # CREATE NEW CASES BY MONTH DICTIONARY
    months = {}

    i = 0
    for date in date_lst:
        if date[:7] not in months.keys():
            months[date[:7]] = new_cases[i]
        elif i == 709: # this spaghetti code prevents the program from breaking, because len(date_lst) is longer than len(new_cases)
            break
        else:
            
            months[date[:7]] += new_cases[i]
        i += 1
        
    # CREATE LISTS FROM THAT DICTIONARY
    most_new_cases_by_month_lst = []
    months2_electric_bugaloo = []
    for key in months.keys():
        most_new_cases_by_month_lst.append(months[key])
        months2_electric_bugaloo.append(key)
    
    # HIGHEST NEW CASES BY MONTH
    most_viral_month = max(most_new_cases_by_month_lst)
    index = most_new_cases_by_month_lst.index(most_viral_month)
    most_viral_month = months2_electric_bugaloo[index]
    country_dict["most_viral_month"] = most_viral_month
    print("Month with the highest new number of confirmed cases:", most_viral_month)
    
    # LOWEST NEW CASES BY MONTH
    least_viral_month = min(most_new_cases_by_month_lst)
    index = most_new_cases_by_month_lst.index(least_viral_month)
    least_viral_month = months2_electric_bugaloo[index]
    country_dict["least_viral_month"] = least_viral_month
    print("Month with the lowest new number of confirmed cases:", least_viral_month)
    
    # JSON DUMPING
    out_file = open("/home/ubuntu/environment/hw3/" + country + ".json", "w")
    json.dump(country_dict, out_file, indent = 6)
    out_file.close()
    
    print("\n")
