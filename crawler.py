import requests
from bs4 import BeautifulSoup


search_url = "http://transcripts.wikia.com/wiki/Cartman_Gets_an_Anal_Probe"

result = requests.get(search_url)
html = result.content.decode("utf-8")
soup = BeautifulSoup(html, features="html.parser")
wikitable = soup.select('table.wikitable')
# print(wikitable)

def crawl_wikia(link):
    result = requests.get(link)
    html = result.content.decode("utf-8")
    soup = BeautifulSoup(html, features="html.parser")
    wikitable = soup.select('table.wikitable')

    read_table(wikitable)

    return True


def read_table(chunk):

    speaker_dict = {}
    current_speaker = ""
    current_text = ""

    for line in chunk:
        if "<th>" in str(line):
            print(current_speaker)
            current_speaker = str(line)[3:].strip(":")
            print(current_speaker)

            if current_speaker not in speaker_dict:
                speaker_dict[current_speaker] = []


        if "<td>" in line:
            current_text = line.strip("<td>", "</th>")
            speaker_dict[current_speaker] = speaker_dict[current_speaker].append(current_text)



    return speaker_dict


def dict_to_json():

    return True


dddd = read_table(wikitable)

print(dddd)
