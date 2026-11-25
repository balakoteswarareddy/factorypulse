
import logging
import random
import time

import requests


logger = logging.getLogger("factorypulse.client")


RETRYABLE_STATUS_CODES = {
    408,
    429,
    500,
    502,
    503,
    504,
}


class TelemetryClient:

    def __init__(
        self,
        endpoint,
        connect_timeout=3,
        read_timeout=5,
        max_attempts=3,
    ):
        self.endpoint = endpoint

        self.timeout = (
            connect_timeout,
            read_timeout,
        )

        self.max_attempts = max_attempts

        self.session = requests.Session()

    def send(self, telemetry):

        telemetry_id = telemetry["telemetry_id"]
        machine_id = telemetry["machine_id"]

        for attempt in range(1, self.max_attempts + 1):

            retry_after = None

            try:
                response = self.session.post(
                    self.endpoint,
                    json=telemetry,
                    timeout=self.timeout,
                    allow_redirects=False,
                )

                if response.status_code in (200, 201):

                    logger.info(
                        "Telemetry delivered: machine=%s "
                        "id=%s status=%s attempt=%s",
                        machine_id,
                        telemetry_id,
                        response.status_code,
                        attempt,
                    )

                    return True

                if (
                    response.status_code
                    not in RETRYABLE_STATUS_CODES
                ):
                    logger.error(
                        "Telemetry rejected: id=%s "
                        "status=%s response=%s",
                        telemetry_id,
                        response.status_code,
                        response.text[:500],
                    )

                    return False

                logger.warning(
                    "Retryable HTTP error: id=%s "
                    "status=%s attempt=%s/%s",
                    telemetry_id,
                    response.status_code,
                    attempt,
                    self.max_attempts,
                )

                retry_after = response.headers.get(
                    "Retry-After"
                )

            except requests.exceptions.SSLError as error:

                logger.error(
                    "TLS verification failed: id=%s error=%s",
                    telemetry_id,
                    error,
                )

                return False

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            ) as error:

                logger.warning(
                    "Communication failure: id=%s "
                    "attempt=%s/%s error=%s",
                    telemetry_id,
                    attempt,
                    self.max_attempts,
                    error,
                )

            except requests.exceptions.RequestException as error:

                logger.error(
                    "HTTP client error: id=%s error=%s",
                    telemetry_id,
                    error,
                )

                return False

            if attempt < self.max_attempts:

                delay = min(2 ** (attempt - 1), 30)

                # Add jitter to avoid synchronized retries.
                delay += random.uniform(0, 0.5)

                # Support Retry-After expressed in seconds.
                if retry_after and retry_after.isdigit():
                    requested_delay = int(retry_after)

                    if requested_delay > 60:
                        logger.warning(
                            "Retry-After exceeds local retry budget"
                        )
                        return False

                    delay = max(delay, requested_delay)

                logger.info(
                    "Retrying telemetry id=%s in %.2f seconds",
                    telemetry_id,
                    delay,
                )

                time.sleep(delay)

        logger.error(
            "Delivery unconfirmed after %s attempts: id=%s",
            self.max_attempts,
            telemetry_id,
        )

        return False

    def close(self):
        self.session.close()
