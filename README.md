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

## Running Locally

The simulator and backend currently run as separate Python processes.

Install the application dependencies:
```bash
python -m pip install -r simulator/requirements.txt
python -m pip install -r backend/requirements.txt
```

Start the backend:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

In another terminal, start the simulator:
```bash
python -m simulator.machine_simulator
```

API documentation is available at http://localhost:8000/docs.

The simulator currently supports configurable HTTP timeouts, limited retries and duplicate-safe telemetry submissions.

Telemetry is temporarily stored in backend process memory. Persistent PostgreSQL storage will be implemented next.

## Documentation

- [Project requirements](docs/requirements.md)
- [Architecture decisions](docs/architecture-decisions/)

## Limitations

This project uses simulated machine telemetry and does not integrate with physical industrial equipment.