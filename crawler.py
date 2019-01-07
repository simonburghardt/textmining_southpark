import requests
from bs4 import BeautifulSoup


search_url = "http://transcripts.wikia.com/wiki/Cartman_Gets_an_Anal_Probe"

result = requests.get(search_url)
html = result.content.decode("utf-8")
soup = BeautifulSoup(html)

print(result.url)

def crawl_wikia(link):
    result = requests.get(link)
    html = result.content.decode("utf-8")
    soup = BeautifulSoup(html)
    wikitable = soup.select('table.wikitable')
    print(wikitable)

    read_table()

    return True


def read_table(soup):

    speaker_dict = {}

    return speaker_dict


def dict_to_json():

    return True

