# ADR-0004: Database Selection

**Date:** 2026-11-25
**Status:** Accepted

## Decision

Initially, I considered SQLite because of its simplicity and my previous experience using it in a Django project.

However, maintaining separate SQLite databases across backend replicas can create inconsistencies in telemetry data.

I chose PostgreSQL so that multiple backend replicas can connect to a common database. Using the same database engine locally and in Azure also reduces compatibility issues during deployment.

For local development, PostgreSQL will run in a Docker container with a persistent volume.

## Trade-offs

PostgreSQL requires additional configuration, network connectivity and database credential management compared to SQLite.

Managed PostgreSQL in Azure also introduces additional cloud costs.

A single database server can still become a single point of failure. Full database redundancy is deferred for the initial version.