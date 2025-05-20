# Overview

High level design for KV Store that replicates to a replica service

# Performance expectations
Able to get around 3K RPS with single threaded KV Store instance.
Replicated version should be slower.

[ ] With two or more replicas:
    1. Try replicated version without async replication from primary
    2. Try replication with async replication calls

# Architecture

Two services: kv-store-1 and kv-store-2
- Hosting
    - Both running on 5001
    - kv-store-1 accessible via localhost:5001
    - kv-store-2 accessible via localhost:5002

Consul registration
- All kv-store instances try to register as primary node and if there is a
    primary already, then register as a replica node
- Primary replicates writes to replicas synchronously
    [ ] How to handle replica success, but primary failure after replicas are successful
