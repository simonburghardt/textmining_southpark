#import main3
import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter
import re
#import main


cursejson = "data/cursewords.json"
databycharacter = "data/dataByCharacter.json"
top20 = ["Cartman", "Stan", "Kyle", "Randy", "Butters", "Mr. Garrison", "Chef", "Mr. Mackey", "Jimmy",
         "Sharon", "Announcer", "Jimbo", "Gerald", "Wendy", "Sheila", "Liane", "Mrs. Garrison",
         "Narrator", "Stephen", "Kenny"]



# Lädt unser Schimpfwort JSON und speichert die in einem Dictionary ab
# z.B. { "a" : ["asshole", "asscow"], "b" : ["bitch", "blowjob"], etc...}
def load_json(data_title):
    fh = open(data_title, mode="r", encoding="utf8")
    ret_dict = json.load(fh)
    return ret_dict


# Tokenized einen gegebenen Text, kickt Stopwords raus und stemt die Wörter
def tokenize_and_stem(text):

    text = text.lower()
    text = text.replace(".", "").replace("!", "").replace(",", "").replace(".?", "") \
        .replace("\r\n", "").lower()
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    tokens = [t for t in tokens if t not in string.punctuation and t not in stopwords.words("english")]
    stems = [PorterStemmer().stem(t) for t in tokens]
    return stems


# Zählt Redebeitraege aus gegebenen Daten und gibt ein Dictionary zurück mit der Anzahl
# der Redebeiträge pro Character.
def count_redebeitraege(input_data):

    speaker_rede = {}
    data = input_data["data"]

    for entry in data:
        character = entry["Character"][0]
        text_liste = entry["Line"]
        token_list = []

        for beitrag in text_liste:
            help_list = tokenize_and_stem(beitrag)
            for eintrag in help_list:
                token_list.append(eintrag)

        speaker_rede[character] = len(token_list)

    sort_dict = sorted(speaker_rede.items(), key=lambda x: x[1], reverse=True)
    return sort_dict


curse_data = load_json(cursejson)
character_data = load_json(databycharacter)
# spoken_tokens = count_redebeitraege(character_data)

