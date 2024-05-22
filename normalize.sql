CREATE TABLE IF NOT EXISTS platforms (
 platform_id INTEGER PRIMARY KEY AUTOINCREMENT,
 platform_name TEXT NOT NULL UNIQUE);

INSERT OR IGNORE INTO platforms (platform_name)
SELECT DISTINCT json_each.value AS name
FROM game_data, json_each(REPLACE(game_data.profile_platforms, '''', '"'))
WHERE game_data.profile_platforms IS NOT NULL
ORDER BY name;

SELECT game_data.game_id AS game_id, platforms.platform_id AS platform_id
FROM game_data JOIN platforms
ON game_data.profile_platforms LIKE '%' || platforms.platform_name || '%';