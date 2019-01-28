import csv
import json
from collections import Counter
global data_dict, data_list, curseword_dict

csv_file = "data/season1.csv"
csv_file1 = "data/all-seasons.csv"
diejson = "data/cursewords.json"

data_list  = []
curseword_dict = {}


# Diese Funktion lädt die Daten aus unserer CSV-Datei in eine Liste. Innerhalb der Liste werden Dictionaries
# für die einzelnen Redebeiträge gespeichert. Beispiel Zeile 1:
# OrderedDict([('Season', '1'), ('Episode', '1'), ('Character', 'Boys'),('Line', "School day, school day,
# teacher's golden ru...\n")])
def load_data():

    # Läd die Datei und speichert den Inhalt in data_dict und die Feldnamen in Header
    with open(csv_file1, 'r+', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            data_list.append(dict(row))

    print('Daten geladen!')
    return True


# Löscht Zeilenumbrüche raus und macht Beitrag zu Kleinbuchstaben
def preprocess(list):

    for entry in list:
        current_line = entry["Line"]
        entry["Line"] = current_line[:-1].lower()

    return True


# Zählt welcher Speaker wie oft gesprochen hat
def count_redebeitraege(data_list):
    speaker = {}
    for s in data_list:
        character = s["Character"]
        if character in speaker:
            speaker[character] += 1
        else:
            speaker[character] = 1

    return speaker


# Tokenized einen übergebenen Text
def tokenize(text):
    tokens = text.split()
    tokens = [t.strip(".,;!?").lower() for t in tokens]
    return tokens


# Filtert alle Sprecher als einem Input heraus
def get_speakers(inp):
    speaker_list = []

    for row in inp:
        if row["Character"] in speaker_list:
            continue
        else:
            speaker_list.append(row["Character"])

    return speaker_list


# Holt sich die kompletten Texte für jeden Sprecher und speichert das in einem Dictionary ab
# Gibt ein Dictionary zurück mit Speaker und dem kompletten Text {"Cartman" : gesamtertext}
def get_whole_text_per_speaker(inp_dict, speaker):

    whole_text_speaker = {}
    alles_zusammen = ""

    for row in inp_dict:
        if row["Character"] == speaker:
            alles_zusammen = str(alles_zusammen + " " + row["Line"])

    whole_text_speaker[speaker] = alles_zusammen

    return whole_text_speaker


# Findet alle Tokens heraus, die ein Speaker sagt
# Übergeben wir eine Liste mit allen Speakern
def get_tokens_per_speaker(inp):

    speaker_most_tokens = {}

    for speaker in inp:
        text_of_speaker = get_whole_text_per_speaker(data_list, speaker)
        speaker_most_tokens[speaker] = dict(Counter(tokenize(text_of_speaker[speaker])))

    return speaker_most_tokens


# Findet heraus, welcher Speaker welche Tokens am öftesten sagt
# Übergeben wir eine Liste mit allen Speakern
def count_tokens_per_speaker(inp_list):

    speaker_tokens = {}

    for speaker in inp_list:
        text_of_speaker = get_whole_text_per_speaker(data_list, speaker)
        speaker_tokens[speaker] = len(tokenize(text_of_speaker[speaker]))

    sort_dict = sorted(speaker_tokens.items(), key=lambda x: x[1], reverse=True)

    return speaker_tokens


# Lädt unser Schimpfwort JSON und speichert die in einem Dictionary ab
# z.B. { "a" : ["asshole", "asscow"], "b" : ["bitch", "blowjob"], etc...}
def loadjson(diejson):
    fh = open(diejson, mode="r", encoding="utf8")
    curseword_dict = json.load(fh)
    return curseword_dict


# Zählt, welcher Speaker wie oft geflucht hat
def count_cursewords_per_speaker(speaker_liste):

    token_counter = 0
    swear_counter = 0
    curseword_dict = loadjson(diejson)

    for speaker in speaker_liste:

        text_of_speaker = get_whole_text_per_speaker(data_list, speaker)
        text_tokens = tokenize(text_of_speaker[speaker])
        token_counter = len(text_tokens)

        for key, value in curseword_dict.items():
            for schimpfwort in value:
                for token in text_tokens:
                    if schimpfwort == token:
                        swear_counter = swear_counter + 1

        rate = swear_counter / token_counter

        print(speaker + " hat " + str(swear_counter) + " Schimpfwörter gesagt mit einer Rate von " + str(rate))
        swear_counter = 0
        token_counter = 0


load_data()
preprocess(data_list)
count_anteile = count_redebeitraege(data_list)
all_speakers = get_speakers(data_list)


count_cursewords_per_speaker(all_speakers)

#print(get_whole_text_per_speaker(data_list, "Jesus"))


