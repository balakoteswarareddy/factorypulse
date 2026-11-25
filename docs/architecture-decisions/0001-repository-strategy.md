# ADR-0001: Repository Strategy

**Date:** 2026-11-24  
**Status:** Accepted

## Context

FactoryPulse is currently a small project, and I am the only contributor working on all its components.

## Decision

I chose a monorepo because it is easier for me to manage and track all the work in one place without switching between repositories.

The application is not currently large or complex enough to justify the additional overhead of maintaining separate repositories for each component.

## Trade-offs

As the project grows, managing component-specific CI pipelines and access permissions may become more difficult.

I will reconsider this decision if the components require independent ownership or repository-level access restrictions.