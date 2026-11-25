# FactoryPulse

FactoryPulse is a cloud-based industrial machine monitoring project. The application collects simulated machine telemetry, stores it and monitors machine health using threshold-based alerts.

## Architecture

- Python simulator running on my local laptop.
- FastAPI backend for telemetry collection and processing.
- PostgreSQL for storing telemetry and alerts.
- Streamlit dashboard for monitoring machine health.

The simulator and dashboard communicate with the backend through REST APIs. Only the backend communicates with the database.

## Technology stack

- Application: Python, FastAPI, Streamlit
- Database: PostgreSQL
- Containerization: Docker, Docker Compose
- CI/CD: GitHub Actions
- Infrastructure as Code: Terraform
- Cloud: Microsoft Azure
- Monitoring: Azure Monitor

## Project status

Currently under development.

- [x] Development environment setup
- [x] Repository setup and branch protection
- [x] Initial architecture design
- [ ] Application development
- [ ] Application testing
- [ ] Containerization
- [ ] CI/CD pipeline
- [ ] Azure infrastructure and deployment
- [ ] Security and monitoring

## Documentation

- [Project requirements](docs/requirements.md)
- [Architecture decisions](docs/architecture-decisions/)

## Limitations

This project uses simulated machine telemetry and does not integrate with physical industrial equipment.