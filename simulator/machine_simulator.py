
import json
import logging
import os
import random
import time
import uuid
from datetime import datetime, timezone

from .telemetry_client import TelemetryClient


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("factorypulse.simulator")


INTERVAL_SECONDS = int(
    os.getenv("TELEMETRY_INTERVAL_SECONDS", "5")
)

ANOMALY_PROBABILITY = float(
    os.getenv("ANOMALY_PROBABILITY", "0.10")
)

TELEMETRY_ENDPOINT = os.getenv(
    "TELEMETRY_ENDPOINT",
    "http://127.0.0.1:8000/api/v1/telemetry",
)

CONNECT_TIMEOUT = float(
    os.getenv("CONNECT_TIMEOUT", "3")
)

READ_TIMEOUT = float(
    os.getenv("READ_TIMEOUT", "5")
)

MAX_ATTEMPTS = int(
    os.getenv("MAX_ATTEMPTS", "3")
)

DRY_RUN = os.getenv(
    "DRY_RUN", "false"
).lower() == "true"

MAX_CYCLES = int(
    os.getenv("MAX_CYCLES", "0")
)


MACHINES = {
    "CNC-01": {
        "temperature": (45.0, 75.0),
        "vibration": (1.0, 4.0),
        "power": (3.0, 8.0),
    },
    "BELT-01": {
        "temperature": (30.0, 55.0),
        "vibration": (0.5, 3.0),
        "power": (1.0, 4.0),
    },
    "MOTOR-01": {
        "temperature": (40.0, 80.0),
        "vibration": (1.0, 5.0),
        "power": (2.0, 6.0),
    },
}


def generate_telemetry(machine_id, config):

    temperature = random.uniform(*config["temperature"])
    vibration = random.uniform(*config["vibration"])
    power = random.uniform(*config["power"])

    if random.random() < ANOMALY_PROBABILITY:
        temperature += random.uniform(20.0, 35.0)
        vibration += random.uniform(3.0, 6.0)

    return {
        "telemetry_id": str(uuid.uuid4()),
        "machine_id": machine_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature_c": round(temperature, 2),
        "vibration_mm_s": round(vibration, 2),
        "power_kw": round(power, 2),
        "operating_status": "RUNNING",
    }


def validate_configuration():

    if INTERVAL_SECONDS <= 0:
        raise ValueError("Telemetry interval must be positive")

    if not 0 <= ANOMALY_PROBABILITY <= 1:
        raise ValueError(
            "Anomaly probability must be between 0 and 1"
        )

    if CONNECT_TIMEOUT <= 0 or READ_TIMEOUT <= 0:
        raise ValueError("Timeouts must be positive")

    if not 1 <= MAX_ATTEMPTS <= 10:
        raise ValueError("MAX_ATTEMPTS must be between 1 and 10")

    if MAX_CYCLES < 0:
        raise ValueError("MAX_CYCLES cannot be negative")


def main():

    validate_configuration()

    client = TelemetryClient(
        endpoint=TELEMETRY_ENDPOINT,
        connect_timeout=int(CONNECT_TIMEOUT),
        read_timeout=int(READ_TIMEOUT),
        max_attempts=MAX_ATTEMPTS,
    )

    generated = 0
    delivered = 0
    unconfirmed = 0
    cycles = 0

    logger.info(
        "Simulator started: machines=%s interval=%ss dry_run=%s",
        len(MACHINES),
        INTERVAL_SECONDS,
        DRY_RUN,
    )

    logger.info("Telemetry endpoint: %s", TELEMETRY_ENDPOINT)

    try:

        while True:

            for machine_id, config in MACHINES.items():

                telemetry = generate_telemetry(
                    machine_id,
                    config,
                )

                generated += 1

                if DRY_RUN:
                    print(json.dumps(telemetry), flush=True)

                elif client.send(telemetry):
                    delivered += 1

                else:
                    unconfirmed += 1

            cycles += 1

            if MAX_CYCLES and cycles >= MAX_CYCLES:
                break

            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        logger.info("Shutdown requested")

    finally:

        client.close()

        logger.info(
            "Simulator stopped: generated=%s "
            "delivered=%s unconfirmed=%s dry_run=%s",
            generated,
            delivered,
            unconfirmed,
            DRY_RUN,
        )


if __name__ == "__main__":
    main()
