CREATE TABLE IF NOT EXISTS platforms (
 platform_id INTEGER PRIMARY KEY AUTOINCREMENT,
 platform_name TEXT NOT NULL UNIQUE);

INSERT OR IGNORE INTO platforms (platform_name)
SELECT DISTINCT json_each.value AS name
FROM game_data, json_each(REPLACE(game_data.profile_platforms, '''', '"'))
WHERE game_data.profile_platforms IS NOT NULL AND name != ''
ORDER BY name;

CREATE TABLE IF NOT EXISTS game_platforms (
game_id INTEGER,
platform_id INTEGER,
PRIMARY KEY (game_id, platform_id),
FOREIGN KEY (game_id) REFERENCES game_data (game_id),
FOREIGN KEY (platform_id) REFERENCES platforms (platform_id)
);

INSERT OR IGNORE INTO game_platforms (game_id, platform_id)
SELECT game_data.game_id AS game_id, platforms.platform_id AS platform_id
FROM game_data JOIN platforms
ON game_data.profile_platforms LIKE '%' || platforms.platform_name || '%';