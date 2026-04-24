-- scripts/schema_setup.sql
-- Creating primary and foreign keys


-- fix data types

alter table movies alter column year type integer using year::integer;

-- primary keys

alter table movies add primary key("movieId");

alter table ratings add primary key("userId","movieId");

--foreign keys

alter table movies_genres 
add constraint fk_movies_genres_movies
foreign key ("movieId") references movies("movieId");

alter table ratings 
add constraint fk_rat_movies
foreign key ("movieId") references movies("movieId");

-- ındexes for performance improving

create index idx_ratings_movieid on ratings("movieId");
create index idx_movies_title on movies("title");