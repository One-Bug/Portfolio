SELECT movies.title FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
WHERE people.name = 'Jennifer Lawrence' AND movies.title IN
    (
        SELECT title FROM movies, stars, people
        WHERE movies.id = stars.movie_id AND
        stars.person_id = people.id AND
        people.name = 'Bradley Cooper'
    )
;
