## 2025-10-01

Test whether throughput is bottlenecked on App Server side: Try load script
with an empty table and see what the throughput is.

## 2025-09-30

Revisiting previous work to see where I left off. Combining some testing from
7/29 and 7/27.

Findings: Can get ~4K RPS. At that point, bottleneck seems to be on client
side (FastAPI instances or Locust) because DB process waits are almost all of
type "Client."

Tested with following config:
- Postgres db in a docker container with ~100M records
    - `make local-up`
- App server running on local machine:
    - `uvicorn api.url_api:app --host 0.0.0.0 --port 8000 --workers 8`
- Using locust testing with script. Only making PUT requests to insert new
records.
    - `locust -f integration-tests/locust-load-test.py`

Results:
- 5 concurrent Locust users: ~2K RPS, not much db wait activity (3 total wait
    events from pg_stat_activity), ~3ms response time (95th %)

    urlshortener=> SELECT state, count(*) FROM pg_stat_activity GROUP BY state;
            state        | count
    ---------------------+-------
                        |     5
    active              |     1
    idle in transaction |     2
    idle                |    35
    (4 rows)


- 20 concurrent Locust users: ~4K RPS, more wait activity (~8 with ~6
    ClientReads), ~7ms response time (95th)

    urlshortener=> SELECT state, count(*) FROM pg_stat_activity GROUP BY state;
            state        | count
    ---------------------+-------
                        |     5
    active              |     3
    idle in transaction |     8
    idle                |    27
    (4 rows)


- 30 concurrent Locust users: ~4K RPS (maybe ~4100), more wait activity (9-12
    ClientReads), ~10ms response time (95th)

    urlshortener=> SELECT state, count(*) FROM pg_stat_activity GROUP BY state;
            state        | count
    ---------------------+-------
                        |     5
    active              |     3
    idle in transaction |    12
    idle                |    23
    (4 rows)


## 2025-07-29

Previous attempts summary:
- Got DB write throughput up over 3K. I think around 4K? Need to test again.
    [ ] Confirm write throughput
    [ ] Record # of Locust and FastAPI workers
- Try reducing DB connection overhead
    [ ] Local DB conn pooling - change get_db() call to keep a persistent
        local session in memory
    [ ] Ext DB conn pooling - pg_bouncer


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