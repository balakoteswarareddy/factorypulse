
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class TelemetryCreate(BaseModel):
    telemetry_id: UUID

    machine_id: Literal[
        "CNC-01",
        "BELT-01",
        "MOTOR-01",
    ]

    timestamp: datetime

    temperature_c: float = Field(
        ge=-50,
        le=300,
    )

    vibration_mm_s: float = Field(
        ge=0,
        le=100,
    )

    power_kw: float = Field(
        ge=0,
        le=1000,
    )

    operating_status: Literal[
        "RUNNING",
        "IDLE",
        "STOPPED",
        "FAULT",
    ]

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, value: datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(
                "Timestamp must include timezone information"
            )

        return value.astimezone(timezone.utc)


class TelemetryRecord(TelemetryCreate):
    received_at: datetime
