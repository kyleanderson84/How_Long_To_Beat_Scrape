import sqlite3
import re
from bs4 import BeautifulSoup as bs
import requests

conn = sqlite3.connect('games.db')
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS genres (game_id INTEGER PRIMARY KEY, genre TEXT);")

conn.commit()

cursor.execute("SELECT game_id FROM game_data;")

headers = {
     'User-Agent':
     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
 }

rows = cursor.fetchall()

cursor.execute("SELECT game_id FROM genres;")
completed_rows = [r[0] for r in cursor.fetchall()]


pattern = re.compile(r'genre', re.IGNORECASE)

row_length = len(rows)
count = 0

for row in rows:
    count += 1
    print((count)/row_length)
    print(row[0])
    if row[0] not in completed_rows:
        page = requests.get("https://howlongtobeat.com/game/" + str(row[0]), headers=headers)
        if page.status_code == 200:
            soup = bs(page.content, "html.parser")
            div = soup.find_all("div", class_='GameSummary_profile_info__HZFQu GameSummary_medium___r_ia')
            for e in div:
                if 'genre' in e.get_text().lower():
                    txt = e.get_text().lower()
                    genreTxt = txt[txt.find(':')+1:].strip()
                    print(genreTxt)
                    cursor.execute('''INSERT INTO genres 
                    (game_id, genre) VALUES (?, ?);
                    ''', (row[0], genreTxt))
                    conn.commit()
