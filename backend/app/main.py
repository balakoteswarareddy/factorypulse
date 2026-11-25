import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi import FastAPI, HTTPException, Response, status

from .schemas import TelemetryCreate, TelemetryRecord


# Application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("factorypulse.backend")


# Initialize the application
app = FastAPI(
    title="FactoryPulse API",
    description="Industrial machine telemetry API",
    version="0.1.0",
)


# Temporary in-memory storage
telemetry_store: dict[UUID, TelemetryRecord] = {}


@app.get("/")
def root():
    return {
        "application": "FactoryPulse",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.post(
    "/api/v1/telemetry",
    response_model=TelemetryRecord,
    status_code=status.HTTP_201_CREATED,
)
async def create_telemetry(
    telemetry: TelemetryCreate,
    response: Response,
):
    existing = telemetry_store.get(telemetry.telemetry_id)

    if existing is not None:
        original_payload = existing.model_dump(
            exclude={"received_at"}
        )

        if original_payload != telemetry.model_dump():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Telemetry ID already exists with different data",
            )

        logger.info(
            "Duplicate telemetry received: %s",
            telemetry.telemetry_id,
        )

        response.status_code = status.HTTP_200_OK
        return existing

    record = TelemetryRecord(
        **telemetry.model_dump(),
        received_at=datetime.now(timezone.utc),
    )

    telemetry_store[record.telemetry_id] = record

    logger.info(
        "Telemetry accepted: machine=%s id=%s",
        record.machine_id,
        record.telemetry_id,
    )

    return record


@app.get(
    "/api/v1/telemetry",
    response_model=list[TelemetryRecord],
)
async def get_telemetry():
    return list(telemetry_store.values())
