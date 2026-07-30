---
title: "SpacetimeDB 2.7 Deep Dive: Folding the Database, Backend, and Realtime Sync into One Agent Runtime"
date: 2026-07-22
source: "https://spacetimedb.com/"
canonical: "https://spacetimedb.com/"
tags:
  - SpacetimeDB
  - Database
  - Backend Runtime
  - Realtime Sync
  - AI Agent
  - Rust
  - TypeScript
  - Game Server
---

# SpacetimeDB 2.7 Deep Dive: Folding the Database, Backend, and Realtime Sync into One Agent Runtime

> **TL;DR:** SpacetimeDB is not "PostgreSQL with realtime subscriptions." It combines a relational database, transactional application logic, RPC, authorization, state synchronization, and client-side caching into one application runtime. Clients subscribe to the rows they need and read them from a local cache; every write goes through a reducer running inside the database. The model is compelling for high-frequency shared state, multiplayer games, collaborative apps, and agent-first teams that want less infrastructure glue. Its costs are a new programming model, in-memory capacity limits, platform coupling, and a BSL 1.1 license rather than a conventional open-source license.

- **Source:** [SpacetimeDB](https://spacetimedb.com/)
- **Version anchor:** [SpacetimeDB v2.7.0, released July 22, 2026](https://github.com/clockworklabs/SpacetimeDB/releases/tag/v2.7.0-hotfix3)
- **Accessed:** 2026-07-30
- **Topic:** relational database / application server / realtime sync / agent backend
- **Tags:** SpacetimeDB / Database / Backend Runtime / Realtime / AI Agent / Rust / TypeScript / Game Server

![SpacetimeDB 2.7 homepage positions the product as a glue-free backend for AI agents](imgs/spacetimedb-agent-backend-runtime/01-spacetimedb-v27-agent-homepage.webp)

## In One Sentence

**SpacetimeDB's real product is not a faster database. It is an application architecture in which the database is the backend.**

A conventional application often looks like this:

`client -> API or game server -> ORM -> database -> cache or queue -> WebSocket sync`

SpacetimeDB tries to collapse the middle into:

`client SDK -> SpacetimeDB module + database`

Developers define tables and business logic in a module. SpacetimeDB compiles that module to WebAssembly or a JavaScript bundle and executes it inside the database runtime. Clients call reducers to write state and subscribe to query results; the server incrementally pushes relevant committed changes into local client caches.

That architecture explains the homepage's new v2.7 message: `Let AI ship the whole backend, glue-free.` The hard part of agent-generated backends is often not writing one endpoint. It is keeping the database schema, server types, client types, authentication, deployment, and realtime state in agreement. SpacetimeDB attempts to remove those joins with one type system and one deployable unit.

## 1. Database, Application Server, and Sync Engine

The [official introduction](https://spacetimedb.com/docs/intro/what-is-spacetimedb/) describes SpacetimeDB as a relational database that is also a server. Application logic is uploaded into the database, and clients do not need a separate web or game server in between.

A SpacetimeDB application revolves around four objects:

| Object | Role | Rough equivalent in a conventional stack |
|---|---|---|
| Table | Stores application state | Relational database table |
| Reducer | Transactional function that changes state | API endpoint + service method + transaction |
| Subscription | Declares which rows a client needs | Query + WebSocket topic + cache invalidation |
| Client SDK | Typed calls and local cache | API client + state store + realtime client |

Server modules currently support Rust, C#, TypeScript, and C++. Client support covers the web and Node.js, Rust, C# and Unity, plus C++ and Unreal Engine. In this model, a database is not merely a data container. It is a deployed application.

![Official SpacetimeDB architecture: clients subscribe to data and call module reducers directly](imgs/spacetimedb-agent-backend-runtime/02-basic-architecture.webp)

The important part of the diagram is not the smaller box count. It is that application logic and data share a runtime. A conventional service may cross a network, a connection pool, and an ORM during every transaction. SpacetimeDB executes transactional logic next to the data.

## 2. A Reducer Is Both an API and a Mandatory Transaction Boundary

[Reducers](https://spacetimedb.com/docs/functions/reducers/) are the core abstraction. Clients cannot update tables arbitrarily; they can only invoke reducers, and every reducer invocation automatically runs as a transaction.

That has three immediate consequences:

1. **Atomicity is the default.** A reducer either commits all of its changes or rolls them all back.
2. **Authorization and writes live together.** Logic can inspect the caller's identity before changing state.
3. **The API schema is generated from code.** Clients use typed bindings rather than a hand-maintained REST contract.

A reducer resembles a stored procedure, but its responsibility is broader. A conventional stored procedure is usually an internal database capability. A reducer is simultaneously application RPC, authorization entry point, transaction, and source of state-change broadcasts. Developers are not writing a little SQL beside the backend; they are defining the backend's command surface.

The hard boundary also imposes constraints. Reducers cannot casually access the filesystem, invoke system calls, or contact external networks because those effects cannot be reliably rolled back with the transaction. Mutable process globals are not persistent state either. Durable state belongs in tables.

This is not a drop-in driver replacement for an existing Node, Django, or Rails service. Adopting it means redrawing the application's boundaries: deterministic transactional logic goes into reducers, while external side effects use a separate path.

## 3. Subscriptions Are Constrained Data Replication, Not Just WebSockets

A client uses a subscription to specify the rows it needs. The server sends the current matching result, followed by incremental changes from committed transactions. The SDK maintains those rows in a local cache, so the UI reads local state rather than fetching the server after every interaction.

![Official subscription and reducer flow: reads arrive through subscriptions while writes go through reducers](imgs/spacetimedb-agent-backend-runtime/03-subscription-reducer-flow.webp)

This is a more complete abstraction than "database plus WebSockets." A conventional realtime backend still asks developers to solve:

- which write triggers which channel;
- whether a message is consistent with the database commit;
- how a reconnecting client catches up;
- how overlapping subscriptions are deduplicated;
- when the UI sees the complete post-transaction state.

[Subscription semantics](https://spacetimedb.com/docs/clients/subscriptions/semantics/) specify update ordering and cache consistency. Client callbacks run after the full cache update, and changes affecting overlapping subscriptions are bundled. The model is closer to continuous replication of query results than to manually broadcasting domain events.

The trade-off is that subscription queries are not arbitrary SQL. They are designed around maintainable sets of rows, not unconstrained analytics, arbitrary aggregation, or heavy batch processing. SpacetimeDB's own documentation describes the system as optimized for low-latency realtime applications rather than analytics.

## 4. Why the Architecture Is Genuinely Attractive for AI Agents

The new AI positioning is not merely a label. Agents generating a backend most often fail at the joins in a conventional stack:

- a migration changes but an ORM type does not;
- an API response changes but the frontend type does not;
- a write succeeds but a cache remains stale;
- a WebSocket event arrives in the wrong client-state order;
- authorization exists on one endpoint but is missed on another;
- local, container, and cloud deployments behave differently.

SpacetimeDB places schema, business functions, and generated client bindings in one chain. An agent can inspect one module to understand the tables, reducers, subscribed data, and types. Version 2.7 also added an [MCP endpoint for standalone databases](https://github.com/clockworklabs/SpacetimeDB/releases/tag/v2.7.0-hotfix3), exposing health, schema, SQL, and reducer invocation tools.

That reduces contextual complexity, but it does not remove product risk. A model can still:

- subscribe to too much data and exhaust bandwidth or memory;
- implement row-level security incorrectly;
- omit an authorization check inside a reducer;
- design a schema that cannot be migrated smoothly;
- repeat external side effects when a procedure transaction retries;
- treat a vendor benchmark as capacity planning for an unrelated workload.

SpacetimeDB gives an agent a smaller and more coherent backend state space. It does not make backend engineering disappear.

## 5. Calling External APIs: Procedures Are the Necessary Escape Hatch

An obvious weakness of "all logic inside the database" is integration with payments, email, model APIs, and webhooks. Current v2.7 documentation provides [procedures](https://spacetimedb.com/docs/functions/procedures/):

- a procedure can make HTTP requests;
- unlike a reducer, it is not automatically wrapped in a transaction;
- database transactions are entered explicitly with `withTx`;
- HTTP requests cannot be awaited while a transaction remains open;
- transaction closures may retry and therefore must remain deterministic.

This is a sensible design that still requires discipline. A procedure can read a job in a short transaction, release it, call an external service, and write the result in another short transaction. The database avoids holding locks across network delays, while idempotency, retries, and compensation return to the application developer.

The documentation still marks procedures in C#, Rust, and C++ as unstable. Products that depend heavily on third-party npm packages, long-running job queues, complex background work, or a large SaaS integration catalog may still find a mature Node backend or a platform such as Convex easier to operate.

## 6. How to Read the 300,000 TPS Claim

SpacetimeDB markets performance improvements of 100 to 1,000 times. Its [updated official benchmark from May 2026](https://spacetimedb.com/blog/benchmarking) reports `303,920 ± 4,712 TPS` for a TypeScript module on a contended fund-transfer workload.

![SpacetimeDB's official contended fund-transfer benchmark, showing throughput and p99 latency over a 300-second run](imgs/spacetimedb-agent-backend-runtime/04-official-contended-benchmark.webp)

The number is interesting, but it must travel with its definition:

- the test compares complete backend paths, not isolated database-engine microbenchmarks;
- the workload has 100,000 accounts and uses an `α=1.5` power-law distribution to create hot-account contention;
- the measurement runs for 300 seconds after a 30-second warm-up;
- SpacetimeDB benefits from colocating logic and data, eliminating network round trips while rows are locked;
- the reproducible rerun uses public single-node SpacetimeDB Standalone, while the original cloud run used a five-node replicated cluster;
- the vendor designed and ran the benchmark.

The company also acknowledged that the first benchmark's SQLite connector contained a bug that prevented update statements from executing, then fixed the connector and reran the tests. Publishing the correction is positive, but it reinforces why the results should not be extrapolated without the code, data distribution, and deployment topology.

The defensible conclusion is not "SpacetimeDB is always 1,000 times faster than Postgres." It is this: **for workloads dominated by hot, short transactions and frequent client synchronization, moving application logic next to the data can remove a major source of latency in a three-tier architecture.**

## 7. BitCraft Demonstrates the Ceiling, Not Universal Fit

SpacetimeDB's strongest production example is Clockwork Labs' own MMORPG, [BitCraft Online](https://bitcraftonline.com/). The company says chat, items, terrain, player positions, and the rest of the backend run as one module, with state synchronized to thousands of players.

That makes the system more than a todo-demo architecture. A multiplayer online game happens to match its strongest workload:

- large amounts of shared state;
- frequent small transactions;
- low-latency state distribution;
- authoritative server logic;
- Unity or Unreal clients;
- pressure to avoid a separate networking protocol for every game system.

BitCraft is also a flagship built by the company behind the database. It shows that the team is willing to carry a real workload on its own system, but it does not replace years of independent validation across more teams and industries.

## 8. Maincloud Meters "Energy," Not Just Requests

[Maincloud pricing](https://spacetimedb.com/pricing) uses TeV credits as a composite usage meter. Scanned and written bytes, index seeks, CPU instructions, egress, and storage are converted into an "energy" cost:

| Plan | Monthly price | Included each month | Typical use |
|---|---:|---:|---|
| Free | $0 | 2,500 TeV | Prototypes, personal projects, low traffic |
| Pro | $25 | 100,000 TeV | Small production apps needing replication and backups |
| Team | $250 | 250,000 TeV | Teams needing permissions and dedicated-node options |
| Enterprise | Custom | Custom | Self-hosting, BYO cloud, custom SLA |

The pricing page describes the Pro allowance as roughly equivalent to 120 million function calls, 500GB of egress, or 40GB of table storage. Those are individual equivalence examples, not simultaneous quotas. Actual cost depends on scan volume, synchronized state, and active data size.

Because application state is held in memory, capacity planning differs from a disk-first database. SpacetimeDB says Maincloud machines can exceed 80 cores and 256GB of RAM, but an individual database remains bounded by physical-machine capacity. Very large cold datasets, analytics history, warehousing, and systems that require arbitrary horizontal sharding are not an automatic fit.

## 9. The Largest Nontechnical Risk: Source-Available, Not Conventional Open Source

The source is public on GitHub, but the current [LICENSE.txt](https://github.com/clockworklabs/SpacetimeDB/blob/master/LICENSE.txt) uses BSL 1.1 and explicitly says, `This License is not an Open Source license`.

At the time of access, the license parameters on the repository's master branch for SpacetimeDB 2.7.1 include:

- rights to copy, modify, redistribute, and make nonproduction use;
- an additional production grant limited to no more than one SpacetimeDB instance;
- no use of the work to provide a Database Service to third parties;
- a commercial license requirement for deployments outside those conditions;
- a change date of July 26, 2031, after which the version moves to AGPL v3 with a linking exception.

This does not mean every application built on SpacetimeDB must be open sourced. It does affect multi-instance self-hosting, hosted services, redistribution, and long-term infrastructure strategy. Teams planning production self-hosting should review the exact license for their version and confirm the intended deployment with the vendor instead of relying on GitHub stars or Docker availability.

There is architectural lock-in as well. Tables, reducers, subscriptions, generated SDKs, identity, and deployment form an integrated model. Migrating back to "Postgres + API + WebSockets" is not a connection-string change; it requires rebuilding the application's boundaries.

## 10. Where It Fits and Where It Does Not

**Prioritize a SpacetimeDB evaluation for:**

- multiplayer games, shared worlds, and realtime collaboration;
- high-frequency short transactions with extensive state synchronization;
- clients that benefit from a typed local cache;
- Rust, C#, TypeScript, or C++ teams;
- small or agent-first teams trying to reduce backend assembly;
- applications willing to adopt modules, reducers, and subscriptions as first-class concepts.

**Validate carefully before committing for:**

- products with many third-party SDKs and background jobs;
- analytics, reporting, full-text search, vector search, or warehousing;
- datasets that clearly exceed a single node's memory envelope;
- workloads dependent on the mature PostgreSQL extension ecosystem;
- unrestricted multi-instance self-hosting or database-as-a-service products;
- stable existing backends that only need one realtime feature.

A good pilot is not a whole-product migration. Choose a genuinely shared-state problem: a multiplayer room, collaborative canvas, realtime task board, or game lobby. Test subscription size, reconnect behavior, authorization, external APIs, schema migrations, and TeV consumption before expanding the commitment.

## Conclusion: It Removes the State-Wiring Layer

SpacetimeDB's most important idea is not the reducer name or a 300,000 TPS chart. It is the definition of a backend as a state runtime:

**tables are state, reducers are transactional commands, subscriptions are continuous queries, and client caches are state replicas.**

That model puts database commits and client-visible state on one pipeline. It reduces duplicated work across APIs, ORMs, cache invalidation, message broadcasting, and type synchronization. For multiplayer games and collaborative applications, that is a powerful abstraction. For AI agents, it offers a smaller and more legible generation target than a conventional collection of cloud services.

But glue-free is not trade-off-free. External side effects, authorization, capacity, migration, observability, metering, and licensing still exist; they have simply changed shape.

Treating SpacetimeDB as a faster Postgres leads to the wrong comparison. Treating it as a relational-data-centered application server gets much closer to the category it is trying to create.

## Primary Sources

- [SpacetimeDB homepage](https://spacetimedb.com/)
- [What is SpacetimeDB?](https://spacetimedb.com/docs/intro/what-is-spacetimedb/)
- [Key architecture concepts](https://spacetimedb.com/docs/intro/key-architecture/)
- [Reducers](https://spacetimedb.com/docs/functions/reducers/)
- [Subscriptions](https://spacetimedb.com/docs/clients/subscriptions/)
- [Procedures](https://spacetimedb.com/docs/functions/procedures/)
- [Official performance benchmark](https://spacetimedb.com/blog/benchmarking)
- [Maincloud pricing](https://spacetimedb.com/pricing)
- [SpacetimeDB GitHub repository](https://github.com/clockworklabs/SpacetimeDB)
- [Business Source License](https://github.com/clockworklabs/SpacetimeDB/blob/master/LICENSE.txt)
