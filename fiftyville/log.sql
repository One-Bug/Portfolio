-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Lock the tables in the db
.tables
-- Lock their schemas
.schema
-- Lock for the crime reports on July 28, 2023 on Humphrey Street
SELECT description
FROM crime_scene_reports
WHERE year = 2023
AND month = 7
AND day = 28
AND street = 'Humphrey Street';
-- Lock for the interviews
SELECT name, transcript
FROM interviews
WHERE year = 2023
AND month = 7
AND day = 28;
-- Lock for the plates as Ruth mention
SELECT hour, minute, activity, license_plate
FROM bakery_security_logs
WHERE year = 2023
AND month = 7
AND day = 28
AND hour = 10
AND minute >= 15 AND minute <= 25;
-- Lock for the owners of the plates
SELECT *
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute >= 15 AND minute <= 25
);
-- Lock for the bank accounts associated to the transaction Eugene declared
SELECT person_id, account_number
FROM bank_accounts
WHERE account_number IN (
    SELECT account_number
    FROM atm_transactions
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND atm_location = 'Leggett Street'
    AND transaction_type ='withdraw';
);
-- Filter the suspects
SELECT name, id
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute >= 15 AND minute <= 25
) AND id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2023
        AND month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type ='withdraw'
    )
);
-- Lock for the people asosiated to the calls as Raymond said and filter the suspects
SELECT name
FROM people
WHERE id IN (
    SELECT DISTINCT id
    FROM people
    WHERE phone_number IN (
    SELECT caller
    fROM phone_calls
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND duration <= 60
    )
) AND id IN (
    SELECT id
    FROM people
    WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute >= 15 AND minute <= 25
) AND id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2023
        AND month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type ='withdraw'
    )
)
);
-- Get the fiftvylle id
SELECT id
FROM airports
WHERE city = 'Fiftyville'
-- Check for the flights as Raymond suggested
SELECT id, destination_airport_id, hour, minute
FROM flights
WHERE origin_airport_id = (
    SELECT id
    FROM airports
    WHERE city = 'Fiftyville'
)
AND year = 2023
AND month = 7
AND day = 29
ORDER BY hour ASC, minute ASC;
-- Check the name of the arriving airport
SELECT city
FROM airports
WHERE id = (
    SELECT destination_airport_id
    FROM flights
    WHERE hour = 8
    AND minute = 20
    AND year = 2023
    AND month = 7
    AND day = 29
);
-- IDENTIFY SUSPECT
SELECT name
FROM people
WHERE passport_number = (
    SELECT passport_number
    FROM passengers
    WHERE flight_id = (
        SELECT id
        FROM flights
        WHERE hour = 8
        AND minute = 20
        AND year = 2023
        AND month = 7
        AND day = 29
        )
) AND name = 'Diana' OR name = 'Bruce';
-- Get Accomplice or who was called by Bruce
SELECT name
FROM people
WHERE phone_number IN (
    SELECT receiver
    FROM phone_calls
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND duration <= 60
    AND caller = (SELECT phone_number FROM people WHERE name = 'Bruce')
)
