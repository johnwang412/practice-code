# Work progress

- TODO:
    - Get a synchronous version of replication running - test this
        - Get primary to replicate to replicas synchronousl

2025-06-26:
    - Hardened Consul interactions - done with this now (though I need to
        write tests ideally)
    - Thought through 2PC semantics and, after some thinking and reading,
        understood more clearly why 2PC doesn't really work if we need actual
        consistency.
    - Next step is to think through log based replication or consensus based
        replication.

2025-06-19:
    - Refactored Consul interaction model to use standard Consul
        recommendations via session kv locking and expiration. Got interaction
        working via separate threads that update uwsgi workers.

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

# Infrastructure overview (as of 2025-05-19)

Using Consul for service registration. Three Consul servers and single agent
that takes API calls.

Three KV Store instances that each try to register as primary. If there is a
primary already, then instances register as replica.