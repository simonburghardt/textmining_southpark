from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


page = requests.get("https://www.rottentomatoes.com/tv/south_park/s22")
soup = BeautifulSoup(page.content, 'html.parser')
clean_html = soup.prettify()
soup2 = BeautifulSoup(clean_html, 'html.parser')
# print(soup2)

# Pattern sucht nach dem Value des Keys "averageScore" und "seasonNumber"
patternScore = re.compile('(?:"averageScore":")(.*?)(?:")')
# patternFilterSpecialCharacters = re.compile('\d+\.\d+')
# Pattern wird mit dem runtergeladenene HTML verglichen und filtert
seasonRating = re.findall(patternScore, soup2.text)
# filtert die Sonderzeichen aus dem Score raus
# seasonRating2 = re.findall(patternFilterSpecialCharacters, str(seasonRating))
# filtert nach Tag <em> um die Seasonnummer zubekommen
seasonInfoHTML = soup2.find_all('em')
# print(seasonInfoHTML[8].getText())
# print(seasonRating)
# Seasonnummer befindet sich an achter Position der Liste
seasonRatingsDict = {seasonInfoHTML[8].getText(): seasonRating}

for a in seasonRatingsDict:
    print(a + ":" + str(seasonRatingsDict[a]))





