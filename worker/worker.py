import requests
from bs4 import BeautifulSoup


def gathering():
    url = "http://www.melon.com/chart/day/index.htm"
    src = requests.get(url)
    souped = BeautifulSoup(src.text, 'lxml')
    print(souped)
