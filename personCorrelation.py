from scipy.stats.stats import pearsonr
import json


def load_json(data_title):
    fh = open(data_title, mode="r", encoding="utf8")
    ret_dict = json.load(fh)
    return ret_dict


schimpfwortratePerSeason = load_json('output/schimpfwortRatePerSeason.json')

swearRateList = []
# User Rating aus Rottentomatoe
ratingList = [4.1, 4.0, 4.2, 4.4, 4.6, 4.6, 4.5, 4.6, 4.4, 4.5, 4.5, 4.3, 4.2, 4.2, 4.1, 4.1, 4.2, 4.3]

# ruft die einzelnen Raten der Schimpfwörter duch alle 18 Seasons auf
for a in schimpfwortratePerSeason:
    for b in a:
        swearRateList.append(a[b])

# Die Funktion rechnet die Korrelation zwischen der Schimpwortrate pro Season zu der UserRating aus
print(pearsonr(swearRateList, ratingList))


