# Work progress

- TODO:
    - Get Aider working with local LLM
    - Get a synchronous version of replication running - test this
        - Get primary to replicate to replicas synchronousl
    - Write logic to register kv store instances as either leader or
        replica
    - Figure out how to kill kv store worker instances (probably
        docker-compose restart cmd)

2025-05-19:
    - UNRESOLVED ERROR: Consul would show a single kv-service registered as both the primary and replica
        - Error stopped occuring...
    - Got instances to register as primary and replica

2025-05-18:
    - Not necessary to put Consul behind Nginx. Should actually be going through
        client instances.

2025-05-16:
    - Working on writing a replicated version of the kv store
    - Got Consul to load up in docker-compose and got the kv store registered

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