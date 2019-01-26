import general_analysis
import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter

databyepisode = general_analysis.load_json("data/dataByEpisode.json")
cursewordlist = general_analysis.create_curse_list()
swearperseason = general_analysis.load_json("output/SwearwordsPerSeason.json")


def create_swearwordlist_per_personandseason(charcter_data_dict, speaker, curselist):

    data = charcter_data_dict["data"]
    character_data = {}
    season_data = {}
    swearlist = []
    season = 1

    while season < 19:
        for entry in data:
            akt_season = entry["Season"]

            if (entry["Character"] == speaker and akt_season == str(season)):
                for beitrag in entry["Line"]:
                    text_tokens = general_analysis.tokenize_and_stem(beitrag)
                    for token in text_tokens:
                        if token in curselist:
                            swearlist.append(token)

        season_data["Season " + str(season)] = Counter(swearlist)
        swearlist = []
        season = season + 1

    character_data[speaker] = season_data

    return character_data




liste = []
for speaker in general_analysis.top20:

    liste.append(create_swearwordlist_per_personandseason(databyepisode, speaker, cursewordlist))

general_analysis.safe_output("SwearwordsPerSeason.json", liste)


