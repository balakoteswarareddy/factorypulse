# Project Requirements

## Objective

FactoryPulse is a platform to monitor the operating health of industrial machines using simulated telemetry.

## Functional requirements

- Collect machine metrics such as temperature, vibration, power consumption and operating status.
- Store the collected metrics with machine IDs and timestamps.
- Retrieve current and historical machine data.
- Compare metrics against defined thresholds and generate alerts when something goes wrong.
- Display machine health and alerts through a dashboard.

## Non-functional requirements

- Telemetry must be securely transferred to the application.
- Only authorized components should access the database.
- Stored data should persist across application restarts.
- Failed telemetry submissions should be handled to reduce data loss.
- The application should support logging, monitoring and future scaling.
- Cloud deployment should stay within the available budget.

## Out of scope

- Physical sensors and PLC integration.
- AI-based analysis.
- Physical machine control.
- Full infrastructure redundancy and disaster recovery in v1.