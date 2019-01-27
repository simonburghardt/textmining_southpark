import general_analysis
import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter

databyepisode = general_analysis.load_json("data/dataByEpisode.json")
dataBySeason = general_analysis.load_json("data/dataBySeason.json")
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


#liste = []
#for speaker in general_analysis.top20:

#    liste.append(create_swearwordlist_per_personandseason(databyepisode, speaker, cursewordlist))

#general_analysis.safe_output("SwearwordsPerSeason.json", liste)

##################


def create_swearlist_per_season(season_data_dict, curselist, speakerlist) :

    data = season_data_dict["data"]
    swearlist = []
    season_data = {}
    season = 1

    while season < 19:
        for entry in data:
            akt_season = entry["Season"]
            currentSpeaker = entry["Character"]

            if akt_season == str(season) and currentSpeaker in speakerlist:
                for beitrag in entry["Line"]:
                    text_tokens = general_analysis.tokenize_and_stem(beitrag)
                    for token in text_tokens:
                        if token in curselist:
                            swearlist.append(token)

        season_data["Season " + str(season)] = Counter(swearlist)
        swearlist = []
        season = season + 1

    return season_data


#seasonCursewordliste = [create_swearlist_per_season(dataBySeason, cursewordlist, general_analysis.top20)]
#general_analysis.safe_output("SwearwordsPerSeason2.json", seasonCursewordliste)


################


def swearwordsPerSeason():
    with open("output/SwearwordsPerSeason2.json") as f:
        dataSwearwordsPerSeason2 = json.load(f)

    seasonnumber = 1
    seasonTotalSwearwords = 0
    seasonSwearData = {}

    while seasonnumber < 2:
        for element in dataSwearwordsPerSeason2:
            for value in element:
                for schimpfwort in element[value]:
                    seasonTotalSwearwords = seasonTotalSwearwords + element[value][schimpfwort]
                    seasonnumber = seasonnumber + 1
                seasonSwearData[value] = seasonTotalSwearwords
                seasonTotalSwearwords = 0

    return seasonSwearData


#totalSwearwordPerSeason = [swearwordsPerSeason()]
#general_analysis.safe_output("totalSwearwordPerSeason.json", totalSwearwordPerSeason)

#####################

def count_tokens2(data_dict, season):

    data = data_dict["data"]
    counter = 0

    for entry in data:
        akt_season = entry["Season"]

        if akt_season == str(season) and entry["Character"] in general_analysis.top20:
            for beitrag in entry["Line"]:
                text_tokens = general_analysis.tokenize_and_stem(beitrag)
                for token in text_tokens:
                    counter = counter + 1
    return counter


def schimpfwortRatePerSeason():
    with open("output/totalSwearwordPerSeason.json") as f:
        swearwordPerSeason = json.load(f)
    season = 1
    swearRatePerSeason = {}

    for element in swearwordPerSeason:
        for key in element:
            swearRatePerSeason[key] = element[key] / count_tokens2(databyepisode, season) * 100
        season = season + 1

    return swearRatePerSeason


totalSwearwordRatePerSeason = [schimpfwortRatePerSeason()]
general_analysis.safe_output("schimpfwortRatePerSeason.json", totalSwearwordRatePerSeason)