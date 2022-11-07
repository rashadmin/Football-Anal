#IMport Library
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException     
import time
from selenium.webdriver.support.ui import Select
import pandas as pd
import numpy as np

# Returns the matches for the selected seasons
def season_select(seasons,season_drop_down,browser):
    season_drop_down.select_by_visible_text(seasons)
    time.sleep(5)
    matches = browser.find_elements('tag name','tr')
    date = [match.find_element('xpath','./td[1]').text for match in matches]
    home_team = [match.find_element('xpath','./td[2]').text for match in matches]
    score= [match.find_element('xpath','./td[3]').text for match in matches]
    away_team= [match.find_element('xpath','./td[4]').text for match in matches]
    season = [seasons for match in matches]
    return date,home_team,score,away_team,season
# Loads the page
def load_page():
    option = Options()
    option.add_argument('start-maximized')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
    browser.get('https://www.adamchoi.co.uk/overs/detailed')
    time.sleep(5)
    all_matches = browser.find_element("xpath",'//label[@analytics-event="All matches"]')
    all_matches.click()
    return browser
#Scrape the selected league
def scraper(country):
    browser = load_page()
    season_list = ['17/18','18/19','19/20','20/21','21/22']
    country_drop_down = Select(browser.find_element('id','country'))
    country_drop_down.select_by_visible_text(country)
    time.sleep(5)
    date_list,home_team_list,score_list,away_team_list,seasons_list = [],[],[],[],[]
    season_drop_down = Select(browser.find_element('id','season'))
    for seasons in season_list:
        date,home_team,score,away_team,season = season_select(seasons,season_drop_down,browser)
        date_list.append(date)
        home_team_list.append(home_team)
        score_list.append(score_list)
        away_team_list.append(away_team)
        seasons_list.append(season)
    date_list,home_team_list = list(np.array(date_list).flatten()),list(np.array(home_team_list).flatten())
    score_list,away_team_list =list(np.array(score_list).flatten()),list(np.array(away_team_list).flatten())
    seasons_list = list(np.array(seasons_list).flatten())
    df = pd.DataFrame(
        {
            'date':date_list,
            'home_team':home_team_list,
            'score':score_list,
            'away_team':away_team_list,
            'season':season_list
        }
    )
    df.name = country
    string = f'{country}_league.csv'
    df.to_csv(string)
    return season_list
