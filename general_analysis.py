import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter

# Diese Datei kreiiert unsere Ausgaben zu unserer generellen Analyse. Unter genereller
# Analyse verstehen wir Daten übergreifend über alle Season. Dadurch möchten wir eine
# generelles Verständnis des Korpus erhalten und Fragen beantworten wie:
# Wer spricht am meisten (absolut)?, Wer schimpft am meisten (absolut)?, Wer hat die höchste Schimpfrate (relativ)?


cursejson = "data/cursewords.json"
databycharacter = "data/dataByCharacter.json"

# Top 20 Charaktere. Diese sind die Charaktere mit den meisten gesprochenen Tokens.
top20 = ["Cartman", "Stan", "Kyle", "Randy", "Butters", "Mr. Garrison", "Chef", "Mr. Mackey", "Jimmy",
         "Sharon", "Announcer", "Jimbo", "Gerald", "Wendy", "Sheila", "Liane", "Mrs. Garrison",
         "Narrator", "Stephen", "Kenny"]


# Lädt ein JSON file in ein Dictionary
def load_json(data_title):
    fh = open(data_title, mode="r", encoding="utf8")
    ret_dict = json.load(fh)
    return ret_dict


# Tokenized einen gegebenen Text. Sonderzeichen werden rausgekickt, Stopwords werden rausgekickt und Wörter werden gestemt
def tokenize_and_stem(text):

    text = text.lower()
    text = text.replace(".", "").replace("!", "").replace(",", "").replace(".?", "") \
        .replace("\r\n", "").replace("(", "").replace(")", "").lower()
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


# Zählt alle Schimpfwörte und alle Tokens, die eine Person sagt in allen Seasons. Anschließend wird eine
# Schimpfwortrate berechnet. (swearwords / tokens) * 100
# Gibt anschließend die Daten in einem Dictionary zurück.
# [{ Charakter : { "Tokens gesamt" : Anzahl, "Swearwords said" : Anzahl, "Swearrate per word" : Rate}, etc... }]
def syndicate_swearing(charcter_data_dict, speaker, curselist):

    data = charcter_data_dict["data"]
    char_data = {}
    counter = 0
    tokencounter = 0
    swear_data = {}

    for entry in data:
        # Es wird abgegleicht, ob der aktuelle Sprecher unser übergebener Speaker ist
        if (entry["Character"][0] == speaker):
            for beitrag in entry["Line"]:
                text_tokens = tokenize_and_stem(beitrag)
                for token in text_tokens:

                    # Zählt die gesagten Tokens
                    tokencounter = tokencounter + 1

                    # Gleicht den Token mit der Schimpfwortliste ab und zählt ggf. hoch
                    if token in curselist:
                        counter = counter + 1

    swear_data["Tokens gesamt"] = tokencounter
    swear_data["Swearwords said"] = counter
    rate = counter/tokencounter * 100
    swear_data["Swearrate per word"] = str(rate) + "%"
    char_data[speaker] = swear_data
    return char_data


# Kreiirt eine Swearword Liste für den übergebenen Speaker und zählt, wie oft er welches
# Schimpfword gesagt hat.
def create_swearwordlist_per_person(charcter_data_dict, speaker, curselist):

    data = charcter_data_dict["data"]
    char_data = {}
    swearlist = []

    for entry in data:
        if (entry["Character"][0] == speaker):
            for beitrag in entry["Line"]:
                text_tokens = tokenize_and_stem(beitrag)
                for token in text_tokens:
                    if token in curselist:
                        swearlist.append(token)

    char_data[speaker] = Counter(swearlist)

    return char_data


# Kreiiert eine Liste die alle Swearwords enthält aus dem Cursedictionary enthält
def create_curse_list():
    curse_data = load_json(cursejson)
    curse_list = []

    for key in curse_data:
        for word in curse_data[key]:
            curse_list.append(word)

    return curse_list


# Kreiirt ein Dictionary das den Speaker und die Anzahl der Schimpfwörter, die diese
# Person gesagt hat
def get_cursewords(speaker_list, param, curselist):

    swearwords_per_speaker = []

    for speaker in speaker_list:

        if param == "Zählen":
            character_swear = syndicate_swearing(character_data, speaker, curselist)
            swearwords_per_speaker.append(character_swear)

        if param == "liste":
            character_sweardict = create_swearwordlist_per_person(character_data, speaker, curselist)
            swearwords_per_speaker.append(character_sweardict)


    return swearwords_per_speaker


# Speichert übergebene Daten in einem JSON File.
def safe_output(dateiname, output_dictionary):
    with open("output/" + dateiname, 'w') as fp:
        json.dump(output_dictionary, fp, indent=4)


# Zählt wie oft Schimpfwörter vorkommen und sortiert diese absteigend.
def topcurswordsoverall(data):

    ret_dict = {}

    for char_data in data:
        for key in char_data:
            single_swear_dict = char_data[key]
            for schimpfwort in single_swear_dict:
                if schimpfwort in ret_dict:
                    ret_dict[schimpfwort] = ret_dict[schimpfwort] + single_swear_dict[schimpfwort]
                else:
                    ret_dict[schimpfwort] = single_swear_dict[schimpfwort]

    sort_dict = dict(sorted(ret_dict.items(), key=lambda x: x[1], reverse=True))

    return sort_dict


# Lädt die Daten pro Charakter in ein Dictionary
character_data = load_json(databycharacter)
curseListsByCharacter = load_json("output/CurseListByCharacter.json")
cursewordlist = create_curse_list()

# Wer flucht am meisten?
# cursecount = get_cursewords(top20, "Zählen", cursewordlist)
# safe_output("CurseDataByCharacter.json", cursecount)


# Wer sagt welche Wörter am meisten?
# curse_liste = get_cursewords(top20, "liste", cursewordlist)
# safe_output("CurseListByCharacter.json", curse_liste)

# top10 = topcurswordsoverall(curseListsByCharacter)
# safe_output("top10cursewords.json", top10)


# cursewords_per_person = get_curseword_count(top20)
# spoken_tokens = count_redebeitraege(character_data)