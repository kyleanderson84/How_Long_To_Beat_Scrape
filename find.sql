SELECT shoote.game_id, shoote.genre_id, shooter.genre_id
FROM
(SELECT game_id, genre_id
FROM game_genre
WHERE genre_id = 249) AS shoote
LEFT JOIN
(SELECT game_id, genre_id
FROM game_genre
WHERE genre_id = 7) AS shooter
ON shoote.game_id = shooter.game_id
;