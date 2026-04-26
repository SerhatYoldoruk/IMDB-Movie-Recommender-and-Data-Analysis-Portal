--Distribution Analysis:

select mg.genres,count(distinct mg."movieId") as movie_count,
round(avg(r.rating)::numeric,2) as avg_score
from movies_genres mg
join ratings r on mg."movieId" = r."movieId" 
group by mg.genres 
order by movie_count desc
limit 5;

-- Ranking analysis
-- using imdb special formula 

with movie_stats as (
	select 
		m.title,m.year,count(r.rating) as v,avg(r.rating) as  R,
		(select avg(rating) from ratings) as C ,
		2500 as m -- at least 2500 votes
	from movies m 
	join ratings r on m."movieId" = r."movieId"
	group by m.title,m.year
	having count(r.rating) >= 2500
)

select title,year,v as vote_count,
		round(R::numeric,2) as raw_score,
		round(((v::numeric /(v+m) * R) + (m::numeric /(v+m) * C))::numeric, 2) as weighted_score
		from movie_stats 
		order by weighted_score desc
		limit 10;
-- Distribution of Genres

select count("movieId") as movie_count, genres from movies_genres
group by genres
order by movie_count desc ;

-- Movie count analysis by years

select year,count(*) as movie_count from movies
where year is not null
group by year
order by year asc;

-- Rating distribution
select rating, count(*) as vote_count
from ratings
group by rating
order by rating;