# Work progress

2025-05-13:
    - Updated app.py and used locust to do some load testing. Getting ~3K RPS
        for single process / thread in-memory KV store.

2025-05-12:
    - Step 1a complete
        - Successfully limited memory on Docker container. KV store OOM'ing.
        - However, KV store OOM'ing randomly when RAM usage is close to max.
          Probably a python thing? Debugging a bit.
    - Step 1b complete
        - RPS with no swap was ~140 RPS
        - RPS with swap was ~40 RPS

# Overview

KV store implementation

Replicated cache
1. Write simple in memory kv store
    a. Don't track memory usage - just get it to work and then deploy to docker
        container that's memory bound and see what errors we get
    b. Confirm that RPS is higher when not swapping to disk
2. Write replication capabilities
3. Write replicated cache with persistence

Distributed cache
1. Write distributed cache
2. Write distributed cache with persistence

# Tips

* Use `docker events --filter container=kv-store` to see Docker system events like OOM kill