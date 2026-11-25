
import json
import os
import random
import time
import uuid
from datetime import datetime, timezone


# Simulator configuration
INTERVAL_SECONDS = int(
    os.getenv("TELEMETRY_INTERVAL_SECONDS", "5")
)

ANOMALY_PROBABILITY = float(
    os.getenv("ANOMALY_PROBABILITY", "0.10")
)


# Machine-specific operating ranges
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

    # Occasionally generate abnormal measurements
    if random.random() < ANOMALY_PROBABILITY:
        temperature += random.uniform(20.0, 35.0)
        vibration += random.uniform(3.0, 6.0)

    telemetry = {
        "telemetry_id": str(uuid.uuid4()),
        "machine_id": machine_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature_c": round(temperature, 2),
        "vibration_mm_s": round(vibration, 2),
        "power_kw": round(power, 2),
        "operating_status": "RUNNING",
    }

    return telemetry


def main():
    if INTERVAL_SECONDS <= 0:
        raise ValueError("Telemetry interval must be positive")

    if not 0 <= ANOMALY_PROBABILITY <= 1:
        raise ValueError("Anomaly probability must be between 0 and 1")

    print("FactoryPulse simulator started")
    print(f"Machines: {len(MACHINES)}")
    print(f"Interval: {INTERVAL_SECONDS} seconds")
    print(f"Anomaly probability: {ANOMALY_PROBABILITY}")

    try:
        while True:
            for machine_id, config in MACHINES.items():
                telemetry = generate_telemetry(
                    machine_id, config
                )

                print(json.dumps(telemetry), flush=True)

            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nFactoryPulse simulator stopped")


if __name__ == "__main__":
    main()
