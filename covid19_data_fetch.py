import requests
import json
from probability_functions import mean, standard_deviation


class HealthCareDistrict(object):

    def __init__(self, name):
        self.name = name
        self.indices = []
        self.infected_total = 0
        self.daily_new = []
        self.stddev_2nd_og = []
        self.infected_cumulative = []
        self.first_order_growths = []
        self.second_order_growths = []


def fetch_data():

    from datetime import timedelta, date

    # API-url for deaths, for later use: https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/finnishCoronaData/v2

    url_whole_fin_whole_year = "https://sampo.thl.fi/pivot/prod/fi/epirapo/covid19case/fact_epirapo_covid19case.json?column=hcdmunicipality2020-445222&row=dateweek2020010120201231-443702L#"
    headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/80.0.3987.162 Safari/537.36"}
    response = requests.get(url_whole_fin_whole_year, headers=headers)
    retrieved_content = json.loads(response.content.decode())["dataset"]
    hcd_names = retrieved_content["dimension"]["hcdmunicipality2020"]["category"]["label"]
    infections = retrieved_content["value"]

    hcds = []
    for name in hcd_names.values():
        hcds.append(HealthCareDistrict(name))


    day_0 = date(2020, 1, 1)
    dates = []
    i = 0
    maximum_value = 0
    '''for value in infections.keys():
        hcds[i].infected_total += int(infections[value])

        if hcds[i].infected_total > maximum_value:
            maximum_value = hcds[i].infected_total
        hcds[i].infected_cumulative.append(hcds[i].infected_total)
        i += 1
        if i > 21:
            date = day_0 + timedelta(days=((int(value)+1) // 22))
            dates.append(date)
            i = 0
    return hcds, dates, maximum_value'''

    # Looping through API data
    # Infections per day are given one by one for each of the 20 districts (hcd) then the total sum for one day,
    # then in the same order for the next day etc
    i = 0
    j = 0
    print(len(list(infections)))
    for value in infections.values():
        daily_new = hcds[i].daily_new
        first_order_growths = hcds[i].first_order_growths
        second_order_growths = hcds[i].second_order_growths
        stddev_2nd_og = hcds[i].stddev_2nd_og

        daily_new.append(int(value))
        if j >= 1:  # Avoiding Index Error
            # Calculating first order growth
            try:
                first_order_growths.append(daily_new[j] / daily_new[j-1])
            except ZeroDivisionError:
                first_order_growths.append(0)

            # Calculating second order growth
            if len(first_order_growths) >= 2:  # Avoiding Index Error
                try:
                    second_order_growths.append(first_order_growths[j-1] / first_order_growths[j-2])
                except ZeroDivisionError:
                    second_order_growths.append(0)
            else:
                second_order_growths.append(0)
            # Calculating STDDEV for 5 previous 2nd order growths
            if len(second_order_growths) >= 5:
                sum = []
                for k in range(0, 4):
                    sum.append(second_order_growths[k-4])
                stddev_2nd_og.append(standard_deviation(sum))
            else:

        i += 1
        if i > 21:  # When all of the hcds for one day are looped over, date will change
            date = day_0 + timedelta(days=((int(value)+1) // 22))
            dates.append(date)
            i = 0
            j += 1
    return hcds, dates, 50
