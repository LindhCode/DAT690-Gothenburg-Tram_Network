from xml.etree.ElementTree import indent
from bs4 import BeautifulSoup
import urllib.request

from numpy import true_divide
from .trams import readTramNetwork
import json

dir_path = "./tram/utils/"

with open(dir_path + "hållplatslista.html", "r", encoding="utf-8") as f:
    html = f.read()

htmlParse = BeautifulSoup(html, 'html.parser')
a_brackets = htmlParse.find_all("a")
stops_and_gid = []
G = readTramNetwork()
for i in a_brackets:
    split_string = i.get_text('href="/reseplanering/hallplatser/').split(",")
    stop_name = split_string[0]
    if stop_name in G.all_stops():
        town = split_string[1]
        if "Göteborg" in town or "Mölndal" in town:
            g_id = i.get("href").split("hallplatser/")[1]
            stops_and_gid.append((stop_name, g_id))

FIRST_PART_URL = "https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&board1Gids="
LAST_PART_URL = "&board1Modules=departures&board1Modules=trafficSituations&board1DepartureSorting=time"

Stop_URL = {}
for name, GID in stops_and_gid:
    Stop_URL[name] = FIRST_PART_URL + GID + LAST_PART_URL

stop_url_fname = dir_path + "/stop_urls.json"
with open(stop_url_fname, "w", encoding="utf-8") as f:
    json.dump(Stop_URL, f, ensure_ascii=False, indent=4)
