import json
import pandas as pd

df = pd.read_csv('data/all-seasons.csv')
dict_groupedByEpisode = []


def get_nested_rec(key, grp):
    rec = {'Season': key[0], 'Episode': key[1], 'Character': key[2]}
    for field in ['Line']:
        rec[field] = list(grp[field].unique())
    return rec


def get_formatted_corpus():
    for key, grp in df.groupby(['Season', 'Episode', 'Character']):
        rec = get_nested_rec(key, grp)
        dict_groupedByEpisode.append(rec)
    return dict_groupedByEpisode


dict_groupedByEpisode = get_formatted_corpus()

dict_groupedByEpisode = dict(data=dict_groupedByEpisode)
# print(json.dumps(dict_groupedByEpisode, indent=4))

with open('data/dataByEpisode.json', 'w') as fp:
    json.dump(dict_groupedByEpisode, fp, indent=4)


####################################

dict_groupedBySeason = []


def get_nested_rec1(key, grp):
    rec = {'Season': key[0], 'Character': key[1]}
    for field in ['Episode', 'Line']:
        rec[field] = list(grp[field].unique())
    return rec


def get_formatted_corpus1():
    for key, grp in df.groupby(['Season', 'Character']):
        rec = get_nested_rec1(key, grp)
        dict_groupedBySeason.append(rec)
    return dict_groupedBySeason


dict_groupedBySeason = get_formatted_corpus1()
dict_groupedBySeason = dict(data=dict_groupedBySeason)
# print(json.dumps(dict_groupedBySeason, indent=4))

with open('data/dataBySeason.json', 'w') as fp:
    json.dump(dict_groupedBySeason, fp, indent=4)

###########################

dict_groupedByCharacter = []

def get_nested_rec2(key, grp):
    rec = {'Character': key[0]}
    for field in ['Character', 'Line']:
        rec[field] = list(grp[field].unique())
    return rec


def get_formatted_corpus2():
    for key, grp in df.groupby(['Character']):
        rec = get_nested_rec2(key, grp)
        dict_groupedByCharacter.append(rec)
    return dict_groupedByCharacter


dict_groupedByCharacter = get_formatted_corpus2()
dict_groupedByCharacter = dict(data=dict_groupedByCharacter)
# print(json.dumps(dict_groupedByCharacter, indent=4))

with open('data/dataByCharacter.json', 'w') as fp:
    json.dump(dict_groupedByCharacter, fp, indent=4)

