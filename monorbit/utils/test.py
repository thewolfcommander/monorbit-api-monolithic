import json
import requests



states = {
    "1":"Andaman and Nicobar Islands",
    "2":"Andhra Pradesh",
    "3":"Arunachal Pradesh",
    "4":"Assam",
    "5":"Bihar",
    "6":"Chandigarh",
    "7":"Chhattisgarh",
    "8":"Dadra and Nagar Haveli",
    "9":"Daman and Diu",
    "10":"Delhi",
    "11":"Goa",
    "12":"Gujarat",
    "13":"Haryana",
    "14":"Himachal Pradesh",
    "15":"Jammu and Kashmir",
    "16":"Jharkhand",
    "17":"Karnataka",
    "18":"Kenmore",
    "19":"Kerala",
    "20":"Lakshadweep",
    "21":"Madhya Pradesh",
    "22":"Maharashtra",
    "23":"Manipur",
    "24":"Meghalaya",
    "25":"Mizoram",
    "26":"Nagaland",
    "27":"Narora",
    "28":"Natwar",
    "29":"Odisha",
    "30":"Paschim Medinipur",
    "31":"Pondicherry",
    "32":"Punjab",
    "33":"Rajasthan",
    "34":"Sikkim",
    "35":"Tamil Nadu",
    "36":"Telangana",
    "37":"Tripura",
    "38":"Uttar Pradesh",
    "39":"Uttarakhand",
    "40":"Vaishali",
    "41":"West Bengal"
}

data = {}
counter = 0
for key, value in states.items():
    key = int(key)
    data[value] = []
    res = requests.get(f'http://lab.iamrohit.in/php_ajax_country_state_city_dropdown/apiv1.php?type=getCities&stateId={key}')
    resp = res.json()["result"]
    for r in resp:
        data[value].append({
            r: resp[r]
        })
    print("{} - Done".format(value))
    counter += 1

with open ('states.json', 'w') as f:
    f.write(json.dumps(data))