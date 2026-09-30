from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import numpy as np

from .users import SimulatedUser, generate_simulated_users


@dataclass
class OTPRequest:
    timestamp: datetime
    user_id: str
    device_id: str
    ip_address: str
    destination_id: str
    country: str
    label: str


def generate_legitimate_traffic(
    users: list[SimulatedUser],
    duration_hours: int = 24,
    average_requests_per_user: float = 2.0,
    seed: int = 42
) -> list[OTPRequest]:
    """
    Generate simulated legitimate OTP requests.

    No real SMS messages are sent.
    Every request is labeled LEGITIMATE for evaluation.
    """

    rng = np.random.default_rng(seed)

    start_time = datetime(2026, 1, 1, 0, 0, 0)

    total_seconds = duration_hours * 60 * 60

    requests = []

    for user in users:

        # Different users make different numbers of requests.
        request_count = rng.poisson(
            average_requests_per_user
        )

        for _ in range(request_count):

            offset_seconds = rng.integers(
                0,
                total_seconds
            )

            timestamp = (
                start_time
                + timedelta(seconds=int(offset_seconds))
            )

            request = OTPRequest(
                timestamp=timestamp,
                user_id=user.user_id,
                device_id=user.device_id,
                ip_address=user.ip_address,
                destination_id=user.destination_id,
                country=user.country,
                label="LEGITIMATE"
            )

            requests.append(request)

    requests.sort(
        key=lambda request: request.timestamp
    )

    return requests


def requests_to_dicts(
    requests: list[OTPRequest]
) -> list[dict]:
    """Convert OTP requests into dictionaries."""

    return [asdict(request) for request in requests]


if __name__ == "__main__":

    users = generate_simulated_users(
        number_of_users=10,
        seed=42
    )

    requests = generate_legitimate_traffic(
        users=users,
        duration_hours=24,
        average_requests_per_user=2.0,
        seed=42
    )

    print(f"Users: {len(users)}")
    print(f"OTP requests: {len(requests)}")
    print()

    for request in requests[:10]:
        print(request)