from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np
import re
from selenium.webdriver.chrome.options import Options
import time

def get_title(anime):
    try:
        return anime.find('h1', 'title-name h1_bold_none').text
    except:
        return "Not Available"

def get_rating(anime):
    try:
        return anime.find('span', {'itemprop':'ratingValue'}).text
    except:
        return "Not Available"

def get_rating_count(anime):
    try:
        return anime.find('span', {'itemprop':'ratingCount'}).text
    except:
        return "Not Available"
    
def get_popularity(anime):
    try:
        return anime.find('span', 'numbers popularity').text
    except:
        return "Not Available"

def get_genres(anime):
    try:
        genres = []
        for genre in anime.find_all('span', {'itemprop':'genre'}):
            genres.append(genre.text)
        return genres
    except:
        return "Not Available"

def get_season(anime):
    try:
        return anime.find('span', 'information season').text
    except:
        return "Not Available"

def get_members(anime):
    try:
        return anime.find('span', 'numbers members').text
    except:
        return "Not Available"

def get_aired(anime):
    try:
        owo = anime.find('span', string='Aired:')

        aired_text = owo.next_sibling.strip()
        data_range_text = aired_text.split(' to ')

        return data_range_text
    except:
        return "Not Available"

def create_a_dataframe(csv_name, animelinks):
    header = ['Title', 'Rating', 'RatingCount', 'Popularity', 'Genre', 'Season', 'Members', 'Aired']
    df = pd.DataFrame(np.array(animelinks), columns=header)
    df.to_csv(csv_name + '.csv', index=False)

def anime_scrape():
    #open a csv file with links of animes
    input_file = "2500test.csv"
    uwu = pd.read_csv(input_file)

    #hides chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    #open google chrome serach engine
    driver = webdriver.Chrome(options=chrome_options)
    anime_info = []

    count = 0
    
    for link in uwu['Link']:
        driver.get(link)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        record = [get_title(soup), get_rating(soup), get_rating_count(soup), get_popularity(soup), get_genres(soup), get_season(soup), get_members(soup), get_aired(soup)]
        anime_info.append(record)
    
    driver.quit()
    
    create_a_dataframe('anime_stats', anime_info)
    

anime_scrape()
