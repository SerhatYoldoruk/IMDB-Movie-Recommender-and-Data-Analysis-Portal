-- scripts/recommendation_logic.sql

WITH target_genres AS (
    SELECT mg.genres FROM movies_genres mg
    JOIN movies m ON mg."movieId" = m."movieId"
    WHERE m.title = 'Toy Story'
),
similar_movies AS (
    SELECT 
        m."movieId", 
        m.title, 
        COUNT(mg.genres) as shared_genres_count
    FROM movies m
    JOIN movies_genres mg ON m."movieId" = mg."movieId"
    WHERE mg.genres IN (SELECT genres FROM target_genres)
      AND m.title <> 'Toy Story'
    GROUP BY m."movieId", m.title
    HAVING COUNT(mg.genres) >= 3 -- at least 3 common genres for similarity
)
SELECT 
    sm.title, 
    sm.shared_genres_count,
    ROUND(AVG(r.rating)::numeric, 2) as avg_rating,
    COUNT(r.rating) as vote_count
FROM similar_movies sm
JOIN ratings r ON sm."movieId" = r."movieId"
GROUP BY sm.title, sm.shared_genres_count
HAVING COUNT(r.rating) >= 500 
ORDER BY sm.shared_genres_count DESC, avg_rating DESC
LIMIT 5;


-- for query speed: 

CREATE MATERIALIZED VIEW movie_rating_stats AS
SELECT 
    "movieId", 
    ROUND(AVG(rating)::numeric, 2) as avg_rating, 
    COUNT(rating) as vote_count
FROM ratings
GROUP BY "movieId";


CREATE INDEX idx_mv_movieid ON movie_rating_stats ("movieId");