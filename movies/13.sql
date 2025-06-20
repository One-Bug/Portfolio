SELECT DISTINCT people.name FROM people
WHERE name != 'Kevin Bacon' AND id IN (
    SELECT stars.person_id FROM stars
    WHERE stars.movie_id IN (
        SELECT movies.id FROM movies, stars, people
        WHERE movies.id = stars.movie_id
        AND people.id = stars.person_id
        AND people.id = stars.person_id AND
        people.name = 'Kevin Bacon' AND people.birth = 1958
    )
)
;
