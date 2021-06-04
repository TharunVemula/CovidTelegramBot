import requests
import json
from datetime import date

datee = date.today().strftime("%d-%m-%Y")


def get_states(link):
    headers = {
        'authority': 'cdn-api.co-vin.in',
        'sec-ch-ua': '^\\^',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'origin': 'https://www.cowin.gov.in',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.cowin.gov.in/',
        'accept-language': 'en-US,en;q=0.9',
        'if-none-match': 'W/^\\^b3-p9LoerRWY+2wRCNojtt6V26onW4^\\^',
    }
    x = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/' + link, headers=headers)
    districts = x.json()["districts"]
    names = []
    codes = []
    for i in districts:
        names.append(i["district_name"])
        codes.append(i["district_id"])
    return [names, codes]


def showcenter(id):
    msg = ""
    id = str(int(id) - 1000)
    center_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="
    center_url = center_url + id + "&date=" + datee
    centers = requests.get(center_url)
    center = centers.json()
    lists = center["centers"]
    if len(lists) == 0:
        msg += "No Vaccination center is available for booking"
        return msg
    else:
        for i in lists:
            for j in i["sessions"]:
                if j["available_capacity"]>0:
                    msg += "Center : " + i["name"] + "\n"
                    msg += "    Available Capacity: " + str(j["available_capacity"]) + "\n"
                    msg += "    Age Limit: " + str(j["min_age_limit"]) + "\n"
        return msg

def pincode(param):
    msg = ""
    center_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="
    center_url = center_url + param + "&date=" + datee
    centers = requests.get(center_url)
    center = centers.json()
    lists = center["centers"]
    if len(lists) == 0:
        msg += "No Vaccination center is available for this pincode\n" \
               "please visit https://www.cowin.gov.in/ for more details"
        return msg
    else:
        for i in lists:
            for j in i["sessions"]:
                if j["available_capacity"] > 0:
                    msg += "Center : " + i["name"] + "\n"
                    msg += "    Available Capacity: " + str(j["available_capacity"]) + "\n"
                    msg += "    Age Limit: " + str(j["min_age_limit"]) + "\n"
        return msg