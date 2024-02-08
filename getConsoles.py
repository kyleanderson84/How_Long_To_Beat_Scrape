import sqlite3
import re
import csv

#This script extracts all platform types from the main table to begin normalizing the data for better analysis

conn = sqlite3.connect('games.db')
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT profile_platforms FROM game_data;")

rows = cursor.fetchall()
results = set()
for row in rows:
    row_list = [s.strip().lower() for s in re.sub(r'[\[\]\'\\"()]','', str(row)).split(',')]
    results.update(row_list)


results = list(results)[1:]

def correct_title(string):
    if string[0].isdigit():
        string = '_' + string
    return string.replace(" ", "_").replace("-", "_").replace("/", "_").replace(".", "_").replace("&", "_and_")

for i in range(len(results)):
    results[i] = correct_title(results[i]) + " BOOLEAN DEFAULT 0"

results_str = ', '.join(results)

print(results_str)

create_table_query = f"CREATE TABLE platforms (id INTEGER PRIMARY KEY, {results_str});"

cursor.execute(create_table_query)

conn.commit()
conn.close()

#with open('platforms.csv', 'w', newline='') as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerow(['Platform'])
#    writer.writerows(map(lambda x: [x], results))
