CREATE TABLE IF NOT EXISTS genre (
 genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
 genre_name TEXT NOT NULL UNIQUE);

INSERT OR IGNORE INTO genre (genre_name)
SELECT DISTINCT TRIM(json_each.value) AS genre
FROM genres, json_each('["' || REPLACE(genres.genre, ',', '","') || '"]')
WHERE genres.genre IS NOT NULL AND genre != '';

CREATE TABLE IF NOT EXISTS game_genre (
game_id INTEGER,
genre_id INTEGER,
PRIMARY KEY (game_id, genre_id),
FOREIGN KEY (game_id) REFERENCES game_data (game_id),
FOREIGN KEY (genre_id) REFERENCES genre (genre_id)
);

INSERT OR IGNORE INTO game_genre (game_id, genre_id)
SELECT genres.game_id AS game_id, genre.genre_id AS genre_id
FROM genres JOIN genre
ON genres.genre LIKE '%' || genre.genre_name || '%';