import sqlite3
import re

conn = sqlite3.connect('games.db')
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT game_id, profile_platforms FROM game_data;")

rows = cursor.fetchall()


def correct_title(string):
    if string[0].isdigit():
        string = '_' + string
    return string.replace(" ", "_").replace("-", "_").replace("/", "_").replace(".", "_").replace("&", "_and_")


for row in rows:
    row_list = [s.strip().lower() for s in re.sub(r'[\[\]\'\\"()]', '', str(row[1])).split(',')]
    for i in range(len(row_list)):
        if len(row_list[i]) > 0:
            row_list[i] = correct_title(row_list[i])
    print(', '.join(row_list))
    print(row[0])
    if len(row_list[0gvfu]) > 0:
        cursor.execute(f"INSERT INTO platforms (id, {', '.join(row_list)}) VALUES ({str(row[0])}, {', '.join(['1' for i in range(len(row_list))])});")
    conn.commit()

conn.close()