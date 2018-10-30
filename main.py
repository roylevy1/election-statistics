import requests
from bs4 import BeautifulSoup
import time
import datetime

MAX_ELECTORS = 182983
links = {
    "votes": "https://services7.arcgis.com/gvSC24scGQBSxl3v/arcgis/rest/services/retzef_JS_election_WGS_1984_Atar_tsiburi/FeatureServer/0/query?f=json&where=(UPPER(muni_heb)%20%3D%20UPPER(%27%D7%90%D7%A9%D7%93%D7%95%D7%93%27))&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A3848510.131586918%2C%22ymin%22%3A3731694.212856393%2C%22xmax%22%3A3868135.3385991105%2C%22ymax%22%3A3744516.5243512136%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%2C%22latestWkid%22%3A3857%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22VotersInRa%22%2C%22outStatisticFieldName%22%3A%22VOTERSINRA_SUM%22%7D%5D&outSR=102100",
    "avg": "https://services7.arcgis.com/gvSC24scGQBSxl3v/arcgis/rest/services/retzef_JS_election_WGS_1984_Atar_tsiburi/FeatureServer/0/query?f=json&where=(UPPER(muni_heb)%20%3D%20UPPER(%27%D7%90%D7%A9%D7%93%D7%95%D7%93%27))&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A3847564.22336189%2C%22ymin%22%3A3720964.3650108753%2C%22xmax%22%3A3888305.1594378343%2C%22ymax%22%3A3746608.9880005177%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outStatistics=%5B%7B%22statisticType%22%3A%22avg%22%2C%22onStatisticField%22%3A%22vs2013%22%2C%22outStatisticFieldName%22%3A%22VS2013_AVG%22%7D%5D&outSR=102100"}
while (datetime.datetime.now().hour < 22):
    page = requests.get(links["votes"])
    soup = BeautifulSoup(page.text, 'html.parser')
    vote = str(soup).split('"VOTERSINRA_SUM":')[1].split("}")[0]
    vote = int(vote)

    page = requests.get(links["avg"])
    soup = BeautifulSoup(page.text, 'html.parser')
    old = str(soup).split('"VS2013_AVG":')[1].split("}")[0]
    old = str(float(old) * 100) + "%"

    current_avg = vote / MAX_ELECTORS * 100

    file = open("stats.txt", "a")
    file.write(str(vote) + "\n")
    file.write(str(current_avg) + "\n")
    file.write(old + "\n")
    file.write(str(time.strftime("%X")) + "\n")
    file.write("\n")
    file.close()

    time.sleep(60)

print("happy end election")