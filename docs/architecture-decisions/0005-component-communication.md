# ADR-0005: Component Communication

**Date:** 2026-11-25
**Status:** Accepted

## Decision

I chose to have the dashboard communicate with the backend API instead of directly accessing the database. This restricts database access to the backend and avoids exposing database credentials to other application components.

The telemetry simulator will run on my local laptop to represent machines operating outside the cloud environment.

The dashboard and telemetry ingestion API will be accessible over HTTPS, while the database will remain private. Access to the backend API must be authenticated.

## Trade-offs

The simulator depends on internet connectivity and backend availability to submit telemetry.

Failed submissions must be handled through retries and appropriate error handling to reduce the risk of data loss.

Database unavailability will affect telemetry storage and retrieval.

A public ingestion endpoint introduces additional security risks that must be addressed through authentication, authorization and request validation.