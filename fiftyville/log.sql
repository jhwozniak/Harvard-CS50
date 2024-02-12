-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Find crime scene description
SELECT description
FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28
AND street = 'Humphrey Street';

-- From crime scene decription I found out that there were 3 witnesses.
-- Here is the query of the witnesses table from that day:
SELECT transcript
FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28;

-- Checking the bakery_security_logs from the day of the crime,
-- following first interviewee's information abouth the thief exiting the bakery and driving away
SELECT *
FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit';

--checking bakery_security_logs' exits from 10am (list of thief suspects):
SELECT *
FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10;

-- Checking atm_transactions table from the day of the crime at Leggett Street,
-- following second interviewee's information abouth suspect withdrawing money before the crime took place (list of thief suspects)
SELECT *
FROM atm_transactions
WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Checking phone_calls table for information about suspect,
-- following third interviewee's information that the thief was ordering someone on the phone to purchase plane tickets for July 29th
-- sorting in ascending order to find the shortest calls (less than minute) (list of thief/accomplice suspects)
SELECT *
FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28
ORDER BY duration ASC;

--checking flights from Fiftyville on 29th July
SELECT *
FROM flights
JOIN airports ON airports.id = flights.origin_airport_id
WHERE year = 2021 AND month = 7 AND day = 29;

--checking destinations of flights from Fiftyville on 29th July (list of suspected escape destinations)
SELECT *
FROM flights
JOIN airports ON airports.id = flights.destination_airport_id
WHERE year = 2021 AND month = 7 AND day = 29
AND flights.origin_airport_id =
(
    SELECT id
    FROM airports
    WHERE city = 'Fiftyville'
)
ORDER BY hour ASC;


--show me data about people who were withdrawing money from atm at Leggett Street on the crime day (list of thief suspects)
SELECT *
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE account_number IN
(
    SELECT account_number
    FROM atm_transactions
    WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
);

--show me data about people who were withdrawing money from atm at Leggett Street on the crime day and
--whose license_plate was recorded at bakery_security_logs between 10:00am and 10:59am: (list of thief suspects)
SELECT *
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE account_number IN
(
    SELECT account_number
    FROM atm_transactions
    WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
)
AND people.license_plate IN
(
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10
);

-- who of the above people was a caller on 28th July? (list of thief suspects)
SELECT name
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE account_number IN
(
    SELECT account_number
    FROM atm_transactions
    WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
)
AND people.license_plate IN
(
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10
)
AND people.phone_number IN
(
    SELECT caller
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28
);


--show passport numbers of passengers of all the outgoing flights from Fiftyville
SELECT passengers.passport_number, flights.hour, flights.minute, airports.city
FROM flights
JOIN airports ON airports.id = flights.destination_airport_id
JOIN passengers ON passengers.flight_id = flights.id
WHERE year = 2021 AND month = 7 AND day = 29
AND flights.origin_airport_id =
(
    SELECT id
    FROM airports
    WHERE city = 'Fiftyville'
)
ORDER BY hour ASC;

--which of these passport numbers are on thieves' suspect list?

SELECT passengers.passport_number, flights.hour, flights.minute, airports.city
FROM flights
JOIN airports ON airports.id = flights.destination_airport_id
JOIN passengers ON passengers.flight_id = flights.id
WHERE year = 2021 AND month = 7 AND day = 29
AND flights.origin_airport_id =
(
    SELECT id
    FROM airports
    WHERE city = 'Fiftyville'
)
AND passengers.passport_number IN
(
    SELECT people.passport_number
    FROM people
    JOIN bank_accounts ON people.id = bank_accounts.person_id
    WHERE account_number IN
    (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
    )
    AND people.license_plate IN
    (
        SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10
    )
    AND people.phone_number IN
    (
        SELECT caller
        FROM phone_calls
        WHERE year = 2021 AND month = 7 AND day = 28
    )
)
ORDER BY hour ASC;

--show persons names on thieves' shortlist:

SELECT name, passport_number
FROM people
WHERE passport_number IN
(
    SELECT passengers.passport_number
    FROM flights
    JOIN airports ON airports.id = flights.destination_airport_id
    JOIN passengers ON passengers.flight_id = flights.id
    WHERE year = 2021 AND month = 7 AND day = 29
    AND flights.origin_airport_id =
    (
        SELECT id
        FROM airports
        WHERE city = 'Fiftyville'
    )
    AND passengers.passport_number IN
    (
        SELECT people.passport_number
        FROM people
        JOIN bank_accounts ON people.id = bank_accounts.person_id
        WHERE account_number IN
        (
            SELECT account_number
            FROM atm_transactions
            WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
        )
        AND people.license_plate IN
        (
            SELECT license_plate
            FROM bakery_security_logs
            WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10
        )
        AND people.phone_number IN
        (
            SELECT caller
            FROM phone_calls
            WHERE year = 2021 AND month = 7 AND day = 28
        )
    )
    ORDER BY hour ASC
);

--shortlist: Bruce (NY), Taylor (NY), Diana (Boston)
--accomplice: who was the receiver of the calls made by the people above?
--show me telephone numbers of these people:

SELECT name, phone_number
FROM people
WHERE passport_number IN
(
    SELECT passengers.passport_number
    FROM flights
    JOIN airports ON airports.id = flights.destination_airport_id
    JOIN passengers ON passengers.flight_id = flights.id
    WHERE year = 2021 AND month = 7 AND day = 29
    AND flights.origin_airport_id =
    (
        SELECT id
        FROM airports
        WHERE city = 'Fiftyville'
    )
    AND passengers.passport_number IN
    (
        SELECT people.passport_number
        FROM people
        JOIN bank_accounts ON people.id = bank_accounts.person_id
        WHERE account_number IN
        (
            SELECT account_number
            FROM atm_transactions
            WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
        )
        AND people.license_plate IN
        (
            SELECT license_plate
            FROM bakery_security_logs
            WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10
        )
        AND people.phone_number IN
        (
            SELECT caller
            FROM phone_calls
            WHERE year = 2021 AND month = 7 AND day = 28
        )
    )
    ORDER BY hour ASC
);

--show me list of their calls
SELECT caller, receiver
FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28
AND caller IN
(
    SELECT phone_number
    FROM people
    WHERE passport_number IN
    (
        SELECT passengers.passport_number
        FROM flights
        JOIN airports ON airports.id = flights.destination_airport_id
        JOIN passengers ON passengers.flight_id = flights.id
        WHERE year = 2021 AND month = 7 AND day = 29
        AND flights.origin_airport_id =
        (
            SELECT id
            FROM airports
            WHERE city = 'Fiftyville'
        )
        AND passengers.passport_number IN
        (
            SELECT people.passport_number
            FROM people
            JOIN bank_accounts ON people.id = bank_accounts.person_id
            WHERE account_number IN
            (
                SELECT account_number
                FROM atm_transactions
                WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
            )
            AND people.license_plate IN
            (
                SELECT license_plate
                FROM bakery_security_logs
                WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10
            )
            AND people.phone_number IN
            (
                SELECT caller
                FROM phone_calls
                WHERE year = 2021 AND month = 7 AND day = 28
            )
        )
        ORDER BY hour ASC
    )
);

--list names of these callers
SELECT name
FROM people
WHERE phone_number IN
(
    SELECT caller
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28
    AND caller IN
    (
        SELECT phone_number
        FROM people
        WHERE passport_number IN
        (
            SELECT passengers.passport_number
            FROM flights
            JOIN airports ON airports.id = flights.destination_airport_id
            JOIN passengers ON passengers.flight_id = flights.id
            WHERE year = 2021 AND month = 7 AND day = 29
            AND flights.origin_airport_id =
            (
                SELECT id
                FROM airports
                WHERE city = 'Fiftyville'
            )
            AND passengers.passport_number IN
            (
                SELECT people.passport_number
                FROM people
                JOIN bank_accounts ON people.id = bank_accounts.person_id
                WHERE account_number IN
                (
                    SELECT account_number
                    FROM atm_transactions
                    WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
                )
                AND people.license_plate IN
                (
                    SELECT license_plate
                    FROM bakery_security_logs
                    WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10
                )
                AND people.phone_number IN
                (
                    SELECT caller
                    FROM phone_calls
                    WHERE year = 2021 AND month = 7 AND day = 28
                )
            )
            ORDER BY hour ASC
        )
    )
);


--list names of these receivers
SELECT name
FROM people
WHERE phone_number IN
(
    SELECT receiver
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28
    AND caller IN
    (
        SELECT phone_number
        FROM people
        WHERE passport_number IN
        (
            SELECT passengers.passport_number
            FROM flights
            JOIN airports ON airports.id = flights.destination_airport_id
            JOIN passengers ON passengers.flight_id = flights.id
            WHERE year = 2021 AND month = 7 AND day = 29
            AND flights.origin_airport_id =
            (
                SELECT id
                FROM airports
                WHERE city = 'Fiftyville'
            )
            AND passengers.passport_number IN
            (
                SELECT people.passport_number
                FROM people
                JOIN bank_accounts ON people.id = bank_accounts.person_id
                WHERE account_number IN
                (
                    SELECT account_number
                    FROM atm_transactions
                    WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
                )
                AND people.license_plate IN
                (
                    SELECT license_plate
                    FROM bakery_security_logs
                    WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10
                )
                AND people.phone_number IN
                (
                    SELECT caller
                    FROM phone_calls
                    WHERE year = 2021 AND month = 7 AND day = 28
                )
            )
            ORDER BY hour ASC
        )
    )
);

--to whom was Taylor calling (duration < 100)?
SELECT name
FROM people
WHERE phone_number IN
(
    SELECT receiver
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28
    AND caller IN
    (
        SELECT phone_number
        FROM people
        WHERE name = 'Taylor'
    )
    AND duration < 100
);

--to whom was Bruce calling (duration < 100)?
SELECT name
FROM people
WHERE phone_number IN
(
    SELECT receiver
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28
    AND caller IN
    (
        SELECT phone_number
        FROM people
        WHERE name = 'Bruce'
    )
    AND duration < 100
);

--to whom was Diana calling (duration < 100)?
SELECT name
FROM people
WHERE phone_number IN
(
    SELECT receiver
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28
    AND caller IN
    (
        SELECT phone_number
        FROM people
        WHERE name = 'Diana'
    )
    AND duration < 100
);

--show me names of passengers of flights 8:20am NY
SELECT name
FROM people
WHERE passport_number IN
(
    SELECT passengers.passport_number
    FROM flights
    JOIN airports ON airports.id = flights.destination_airport_id
    JOIN passengers ON passengers.flight_id = flights.id
    WHERE year = 2021 AND month = 7 AND day = 29
    AND flights.destination_airport_id =
    (
        SELECT id
        FROM airports
        WHERE city = 'New York City'
    )
);

--show me names of passengers of flights 16:00 BOS
SELECT name
FROM people
WHERE passport_number IN
(
    SELECT passengers.passport_number
    FROM flights
    JOIN airports ON airports.id = flights.destination_airport_id
    JOIN passengers ON passengers.flight_id = flights.id
    WHERE year = 2021 AND month = 7 AND day = 29
    AND flights.destination_airport_id =
    (
        SELECT id
        FROM airports
        WHERE city = 'Boston'
    )
);

--names of atm withdrawees
SELECT name
FROM people
WHERE id IN
(
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN
    (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
    )
);

--names of license_plates exiting bakery:
SELECT name
FROM people
WHERE license_plate IN
(
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10
);

--names of callers on that day (duration < 60)
SELECT name
FROM people
WHERE phone_number IN
(
    SELECT caller
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
);

--receivers of Taylor calls (duration <60)
--to whom was Taylor, Diana, Bruce calling (duration < 100)?
SELECT name
FROM people
WHERE phone_number IN
(
    SELECT receiver
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28
    AND caller IN
    (
        SELECT phone_number
        FROM people
        WHERE name = 'Taylor'
    )
    AND duration < 60
);

SELECT name
FROM people
WHERE phone_number IN
(
    SELECT receiver
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28
    AND caller IN
    (
        SELECT phone_number
        FROM people
        WHERE name = 'Diana'
    )
    AND duration < 60
);

SELECT name
FROM people
WHERE phone_number IN
(
    SELECT receiver
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28
    AND caller IN
    (
        SELECT phone_number
        FROM people
        WHERE name = 'Bruce'
    )
    AND duration < 60
);

--flights outgoing from Fiftyville on 29th July:
SELECT flights.hour, flights.minute, airports.city, passengers.passport_number, people.name
FROM flights
JOIN airports ON airports.id = flights.destination_airport_id
JOIN passengers ON passengers.flight_id = flights.id
JOIN people ON people.passport_number = passengers.Passport_number
WHERE year = 2021 AND month = 7 AND day = 29
AND flights.origin_airport_id =
(
    SELECT id
    FROM airports
    WHERE city = 'Fiftyville'
)
ORDER BY people.name ASC;

SELECT name
FROM people
WHERE phone_number IN
(
    SELECT receiver
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28
    AND caller =
    (
        SELECT phone_number
        FROM people
        Where name = 'Diana'
    )
);