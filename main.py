import requests
from bs4 import BeautifulSoup
import time
import datetime

SLEEP_TIME = 60
CITY_NAME = "אשדוד"

links = {
    "electors": "https://services7.arcgis.com/gvSC24scGQBSxl3v/arcgis/rest/services/retzef_JS_election_WGS_1984_Atar_tsiburi/FeatureServer/0/query?f=json&where=(UPPER(muni_heb)%20=%20UPPER('" + CITY_NAME + "'))&outStatistics=[{%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Registered%22%2C%22outStatisticFieldName%22%3A%22REGISTERED_SUM%22}]&outSR=102100",
    "votes": "https://services7.arcgis.com/gvSC24scGQBSxl3v/arcgis/rest/services/retzef_JS_election_WGS_1984_Atar_tsiburi/FeatureServer/0/query?f=json&where=(UPPER(muni_heb)%20=%20UPPER('" + CITY_NAME + "'))&outStatistics=[{%22statisticType%22:%22sum%22,%22onStatisticField%22:%22VotersInRa%22,%22outStatisticFieldName%22:%22VOTERSINRA_SUM%22}]&outSR=102100",
    "avg": "https://services7.arcgis.com/gvSC24scGQBSxl3v/arcgis/rest/services/retzef_JS_election_WGS_1984_Atar_tsiburi/FeatureServer/0/query?f=json&where=(UPPER(muni_heb)%20=%20UPPER('" + CITY_NAME + "'))&outStatistics=%5B%7B%22statisticType%22%3A%22avg%22%2C%22onStatisticField%22%3A%22vs2013%22%2C%22outStatisticFieldName%22%3A%22VS2013_AVG%22%7D%5D&outSR=102100"}

page = requests.get(links["electors"])
soup = BeautifulSoup(page.text, 'html.parser')
electors = str(soup).split('"REGISTERED_SUM":')[1].split("}")[0]
max_electors = int(electors)

while (datetime.datetime.now().hour < 22):
    page = requests.get(links["votes"])
    soup = BeautifulSoup(page.text, 'html.parser')
    vote = str(soup).split('"VOTERSINRA_SUM":')[1].split("}")[0]
    vote = int(vote)

    page = requests.get(links["avg"])
    soup = BeautifulSoup(page.text, 'html.parser')
    old = str(soup).split('"VS2013_AVG":')[1].split("}")[0]
    old = str(float(old) * 100) + "%"

    current_avg = vote / max_electors * 100

    file = open("stats.txt", "a")
    file.write(str(vote) + "\n")
    file.write(str(current_avg) + "\n")
    file.write(old + "\n")
    file.write(str(time.strftime("%X")) + "\n")
    file.write("\n")
    file.close()

    time.sleep(SLEEP_TIME)

print("happy end election")
