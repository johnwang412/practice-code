## 2025-07-27

Proposed setup #1
- Locust - run 4 processes / 4 cores for distributed user traffic generation
- Uvicorn - run on localhost with 8 workers
- API - health endpoint only
- TRY to max out connections

Results
- Running naive comparison on local and on docker stack results in a big
    difference: 16K with webserver on local vs 6K on docker
    - each setup with uvicorn 8 workers and 4 locust processes generating load
- Running Locust and webservers on localhost (not docker) and leaving Postgres
    on docker container (out of convenience)
    - averaging 2.8K RPS on PUTs - steady over 1 min
    - still a lot of ClientRead waits in pg_stat_activity
        urlshortener=# SELECT wait_event, count(1)
        FROM pg_stat_activity
        WHERE state <> 'idle' group by wait_event;
        wait_event  | count
        --------------+-------
                    |     1
        DataFileRead |     4
        WALSync      |     1
        WALWrite     |    10
        ClientRead   |    15
        (5 rows)
    - But also some more WALWrite and DataFileRead wait events



## 2025-07-26

Loaded url_mappings table with 100M records
Tested performance: standard docker compose stack with Postgres:15
- Result was very poor inserts at 1.5s for avg response time.
    Looked at my indexes and API logic and I didn't have the right indexes in
    place. Added indexes and latency dropped to 30ms and I got around 2K
    RPS on shortened URL writes.

Then tried to up the throughput on the database as much as possible. Placed a
lot of load against my stack with Locust, and running database pg_stat_activity
query showed that the database was actually waiting for the client:

    SELECT wait_event, count(1)
    FROM pg_stat_activity
    WHERE state <> 'idle' group by wait_event;
    wait_event  | count
    --------------+-------
                |     4
    DataFileRead |     1
    WALSync      |     1
    WALWrite     |     1
    ClientRead   |    27
    (5 rows)

I started looking at maximizing requests from Locust and through the API
servers. Set the API server logic to simply return a string, configured Locust
workers to be more parallel (6-12 workers) and the uvicorn web server to be
more parallel (12-16 workers).

Started running into contention (probably CPU related) so now trying to figure
out what balance gets me the highest,consistent throughput of requests to
Postgres. Observing that, with high concurrency, throughput will be high
initially but drop by something like 50% after a few seconds.