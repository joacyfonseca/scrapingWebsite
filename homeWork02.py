# Homework 02
# Imports
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Web driver path
PATH = "C:/Users/user/Google Drive/BCIT/COMP - 2454 - PYTHON FUNDAMENTALS/Drivers/chromedriver"
browser = webdriver.Chrome(PATH)

# Part A
# Creating the extraction function
def extractText(data):
    text    = data.get_attribute('innerHTML')
    soup    = BeautifulSoup(text, features="lxml")
    content = soup.get_text()
    content = re.sub(r"[\n\t]*", "", content)
    content = re.sub('[ ]{2,}', '', content)
    content = re.sub('[.]$','', content)
    return content

# Creating the class
class Game:
    name        = ''
    score       = ''
    platform    = ''
    release     = ''
    rank        = ''

    def __init__(self,name,score,platform,release,rank):
        self.name       = name
        self.score      = score
        self.platform   = platform
        self.release    = release
        self.rank       = rank

    def showDetails(self):
        print("Game: "      + self.name)
        print("Score: "     + self.score)
        print("Platform: "  + self.platform)
        print("Release: "   + self.release)
        print("Rank: "      + self.rank)

# Creating a Games list to storage the extracted data
gameList = []
startURL = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?sort=desc"
pageNum = 1

for pageNum in range(0,3):
    browser.get(startURL)
    # Selector of each content on the screen
    titles      = browser.find_elements_by_css_selector(".title h3")
    score       = browser.find_elements_by_css_selector(".clamp-metascore .positive")
    platform    = browser.find_elements_by_css_selector(".platform .data")
    release     = browser.find_elements_by_css_selector(".platform+ span")
    rank        = browser.find_elements_by_css_selector(".numbered")
    # Giving the browser time to read the content.
    time.sleep(3)

    # Iterating through the data and storing it inside the list
    for i in range(0,len(titles)):
        gameName        = extractText(titles[i])
        gameScore       = extractText(score[i])
        gamePlatform    = extractText(platform[i])
        gameRelease     = extractText(release[i])
        gameRank        = extractText(rank[i])
        game            = Game(gameName,gameScore,gamePlatform,gameRelease,gameRank)
        gameList.append(game)

    pageNum += 1
    newURL = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?sort=desc&page=" + str(pageNum)
    startURL = newURL

# Printing in a nicely and formatted way.
for game in gameList:
    game.showDetails()
    print("\n")

# Creating the Data Set
data = []
df = pd.DataFrame(data, columns={'Name', 'Score', 'Platform', 'Release', 'Rank'})

for game in gameList:
    dictionary = {'Name': game.name, 'Score': game.score, 'Platform': game.platform, 'Release': game.release, 'Rank': game.rank}
    df = df.append(dictionary, ignore_index=True)

comp2454_folder = 'C:/Users/user/Google Drive/BCIT/COMP - 2454 - PYTHON FUNDAMENTALS/dataSets/'
file_name = 'homework02.csv'

df.to_csv(comp2454_folder + file_name,sep=',')

new_df = pd.read_csv(comp2454_folder + file_name, sep=',')

print(new_df.head(2))
print('-------------------------------------------------------------------------------------------------')
print(new_df.tail(2))

# Part B
# URL and browser initialization
dynamicURL = "https://stats.nba.com/teams/traditional/?sort=PTS&dir=-1&Season=2019-20&SeasonType=Regular%20Season"
browser = webdriver.Chrome(PATH)
browser.get(dynamicURL)

# Selectors
team                = browser.find_elements_by_css_selector(".first a")
games_played        = browser.find_elements_by_css_selector(".first+ td")
wins                = browser.find_elements_by_css_selector("td:nth-child(4)")
defeats             = browser.find_elements_by_css_selector("td:nth-child(5)")

# Giving the browser time to read the content.
time.sleep(3)

# Creating a Class
class Team:
    name        = ''
    gp          = ''
    wins        = ''
    defeats     = ''

    def __init__(self,name,gp,wins,defeats):
        self.name       = name
        self.gp         = gp
        self.wins       = wins
        self.defeats    = defeats

teamList = []

# Looping through the selectors and extracting the data
for i in range(0,len(team[0:30])):
    teamName        = extractText(team[i])
    teamGp          = extractText(games_played[i])
    teamWins        = extractText(wins[i])
    teamDefeats     = extractText(defeats[i])
    teamObject = Team(teamName,teamGp,teamWins,teamDefeats)
    teamList.append(teamObject)

# Creating a Data frame
teamData = []
team_df = pd.DataFrame(teamData, columns={'Name', 'Games Played', 'Wins', 'Defeats'})

# Looping through the team list.
for team in teamList:
    teamDictionary = {'Name': team.name, 'Games Played': team.gp, 'Wins': team.wins, 'Defeats': team.defeats}
    team_df = team_df.append(teamDictionary, ignore_index=True)

# Converting some columns to int
team_df['Games Played'] = team_df['Games Played'].astype('int64')
team_df['Wins'] = team_df['Wins'].astype('int64')
team_df['Defeats'] = team_df['Defeats'].astype('int64')

# Creating the input
print('How many teams do you want to see on the graph ? Recommended is 5')
num_teams = input()
num_teams = int(num_teams)

# Creating the graph
graph_01 = team_df[0:num_teams].plot.bar(x='Name', rot= 0)
plt.xlabel("Team")
plt.ylabel("Games/Wins/Defeats")
plt.title("Stats of NBA teams for the season: Games Played | Wins | Defeats")