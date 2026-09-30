from dataclasses import asdict
from datetime import datetime, timedelta
import numpy as np

from .users import SimulatedUser
from .legitimate import OTPRequest


def generate_high_volume_attack(
    users: list[SimulatedUser],
    duration_hours: int = 24,
    number_of_attackers: int = 10,
    requests_per_attacker: int = 1000,
    seed: int = 42
) -> list[OTPRequest]:
    """
    Generate simulated high-volume AIT traffic.

    This attack represents a small number of simulated attacker
    sources generating a large number of OTP requests.

    No real SMS messages or network traffic are generated.
    """

    rng = np.random.default_rng(seed)

    start_time = datetime(2026, 1, 1, 0, 0, 0)
    total_seconds = duration_hours * 60 * 60

    requests = []

    # Select simulated users whose attributes can serve as
    # attacker sources.
    attacker_users = users[:number_of_attackers]

    for attacker_number, attacker in enumerate(attacker_users, start=1):

        for request_number in range(requests_per_attacker):

            # Spread attack requests throughout the simulation period.
            offset_seconds = rng.integers(
                0,
                total_seconds
            )

            timestamp = (
                start_time
                + timedelta(seconds=int(offset_seconds))
            )

            # Give attack requests unique simulated destinations.
            destination_id = (
                f"attack_destination_"
                f"{attacker_number:04d}_"
                f"{request_number:06d}"
            )

            request = OTPRequest(
                timestamp=timestamp,
                user_id=f"attacker_{attacker_number:04d}",
                device_id=f"attack_device_{attacker_number:04d}",
                ip_address=f"198.51.100.{attacker_number}",
                destination_id=destination_id,
                country=attacker.country,
                label="AIT"
            )

            requests.append(request)

    requests.sort(
        key=lambda request: request.timestamp
    )

    return requests


def requests_to_dicts(
    requests: list[OTPRequest]
) -> list[dict]:
    """Convert attack requests into dictionaries."""

    return [asdict(request) for request in requests]


if __name__ == "__main__":

    from .users import generate_simulated_users

    users = generate_simulated_users(
        number_of_users=100,
        seed=42
    )

    attack_requests = generate_high_volume_attack(
        users=users,
        duration_hours=24,
        number_of_attackers=10,
        requests_per_attacker=1000,
        seed=42
    )

    print(f"Attack requests: {len(attack_requests)}")
    print()

    for request in attack_requests[:10]:
        print(request)