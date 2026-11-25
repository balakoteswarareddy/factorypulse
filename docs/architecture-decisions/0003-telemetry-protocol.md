# ADR-0003: Telemetry Communication Protocol

**Date:** 2026-11-25  
**Status:** Accepted

## Decision

I chose HTTP REST for telemetry ingestion because the current scale of FactoryPulse is small, with only three simulated machines.

REST provides a simpler implementation without the additional configuration and maintenance of an MQTT message broker.

Since we are not integrating physical IoT devices or handling large-scale telemetry at this stage, MQTT is not necessary for the current requirements.

## Trade-offs

With REST, the simulator depends directly on the availability of the backend API. Failed requests, retries and duplicate telemetry must be handled by the application.

I will reconsider MQTT if the project expands to include constrained IoT devices, unreliable network connections or a larger number of telemetry producers.