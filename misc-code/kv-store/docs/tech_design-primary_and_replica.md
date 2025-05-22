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

# Replication

## Option 1

Each primary replication request has an incrementing ID. When primary fails,
the replica with greatest ID is elected leader.
- How do replicas compare IDs?
    - Use election/<replica_id>/<replication_sequence_number> as the key to
        report ids on
    - Each replica enumerates its neighbors in the replica group and then
        waits until all sequence numbers are in
    - Each replica then attempts to become the leader only if it has the
        highest sequence number
    - Once a leader is elected, it clears sequence numbers
        If the leader fails at this point, the sequence numbers are still
        accurate.
        IMPLICATION is that replicas should only check if all active replicas
        have a sequence number and not that there are as many sequence nubmers
        as active replicas.
    [ ] Sequence numbers probably need to be written to disk

[ ] How to determine whether the leader is truly down? What if leader comes back after long
    network partition and a new leader already exists? (use generation numbers)

[ ] How does new leader know what to replicate to new followers that may be behind?
