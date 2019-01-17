import requests
import re
import string
import json
from bs4 import BeautifulSoup


search_url = "https://www.noswearing.com/dictionary/{}"

# Liefert uns das komplette Alphabet als Liste
alphabet = list(string.ascii_lowercase)


# HTML Request auf Dicitonary Seite. Liefert fett gedruckte Tags zurück
def crawl_sweardict(link, buchstabe):
    result = requests.get(link.format(buchstabe))
    html = result.content.decode("utf-8")
    soup = BeautifulSoup(html, features="html.parser")
    chunk = soup.select('b')

    return chunk


# Tokenisiert einen Text und entfernt Satzzeichen
def tokenize(text):
    tokens = text.split()
    tokens = [t.strip(".,;!?").lower() for t in tokens]
    return tokens


def filter_list(chunk):

    swearword_list = []

    for entry in chunk:

        # Filtert HTML Tags raus
        p = re.compile(r'<.*?>')
        entry = p.sub('', str(entry))

        # Checkt, ob das Schimpfwort aus mehr als 2 Wörtern besteht und filtert ggf.
        if len(tokenize(entry)) > 2:
            continue

        # Checkt, ob Nummern im String sind
        elif bool(re.search(r'\d', entry)) == True:
            continue

        # Filtert leere oder Wörter mit 2 Buchstaben raus
        try:
            if entry[1]:
                True
        except:
            continue

        else:
            swearword_list.append(entry)

    return swearword_list


# Generiert ein JSON File aus einem Dictionary
def dict_to_json(parsed_data):

    fh = open('data/' + "cursewords" , mode="w", encoding="utf8")
    json.dump(parsed_data, fh, indent=4)

    return True


def crawl_all_swear_words():

    swearwords_per_buchstabe = {}

    # Crawlt für jeden Buchstaben die Swearword-Seite und speichert die generierte Liste in einem
    # Dictionary ab
    # Beispiel: { "a" : ["asshole", "asscow"], "b" : ["bitch", "blowjob"] }
    for buchstabe in alphabet:
        swearwords_per_buchstabe[buchstabe] = filter_list(crawl_sweardict(search_url, buchstabe))

    return swearwords_per_buchstabe


dict_to_json(crawl_all_swear_words())
