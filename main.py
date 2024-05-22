import requests
import time
import bs4 as bs
import pandas as pd
from io import StringIO
import json
import sqlite3
from howlongtobeatpy import HowLongToBeat

#This is the main script to scrape howlongtobeat.com
#

# main_url = "https://howlongtobeat.com/game/"
# headers = {
#     'User-Agent':
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
# }

conn = sqlite3.connect('games.db')
cursor = conn.cursor()

#Create table to collect data
cursor.execute('''CREATE TABLE IF NOT EXISTS game_data ( 
  game_id INTEGER PRIMARY KEY, 
  game_name TEXT, 
  game_alias TEXT, 
  game_type TEXT, 
  game_image_url TEXT, 
  game_web_link TEXT, 
  review_score REAL, 
  profile_dev TEXT, 
  profile_platforms TEXT,
  release_world TEXT,
  similarity REAL,
  json_content TEXT,
  main_story REAL, 
  main_extra REAL,
  completionist REAL,
  all_styles REAL)''')

conn.commit()

#Find how far we have searched for games to scrape
cursor.execute('''SELECT MAX(game_id) FROM game_data''')

max_id = cursor.fetchone()[0]
if max_id is None:
    max_id = 1
else:
    max_id += 1


#scrape game data one page at time, stopping at 150,000 games
#website claims to have 67k games registered, but a lot of 404s in the id number sequence
#hence the large search
for i in range(max_id, 150000):
    game = HowLongToBeat().search_from_id(i)
    if game is not None:
        game_dict = vars(game)
        cursor.execute(
            '''
        INSERT INTO game_data (game_id, 
        game_name, 
        game_alias, 
        game_type, 
        game_image_url, 
        game_web_link, 
        review_score, 
        profile_dev, 
        profile_platforms, 
        release_world, 
        similarity, 
        json_content, 
        main_story, 
        main_extra, 
        completionist, 
        all_styles) VAlUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (game_dict['game_id'], game_dict['game_name'],
          game_dict['game_alias'], game_dict['game_type'],
          game_dict['game_image_url'], game_dict['game_web_link'],
          game_dict['review_score'], game_dict['profile_dev'],
          str(game_dict['profile_platforms']), game_dict['release_world'],
          game_dict['similarity'], str(game_dict['json_content']),
          game_dict['main_story'], game_dict['main_extra'],
          game_dict['completionist'], game_dict['all_styles']))
        conn.commit()
        print(f"Inserted {i}")

#Code for scraping games main pages, no longer used after finding a library made to scrape data from search api

# for i in range(1, 20):
#   url = main_url + str(i)
#   r = requests.get(url, headers=headers)
#   print(str(i) + " : " + str(r.status_code))
#   cursor.execute(f"INSERT INTO page_status (id, status) VALUES ({i}, {r.status_code})")
#   conn.commit()
#   if r.status_code == 200:
#     soup = bs.BeautifulSoup(r.text, "html.parser")
#     #get general game data
#     game_name_div = soup.find('div', class_='GameHeader_profile_header__q_PID')
#     if game_name_div:
#       game_name = game_name_div.get_text()
#       print(game_name)

#     tables = pd.read_html(StringIO(r.text))

#     print(tables)
#   time.sleep(10)

conn.close()
