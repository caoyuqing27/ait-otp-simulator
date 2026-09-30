from dataclasses import dataclass, asdict
import random
import string


@dataclass
class SimulatedUser:
    user_id: str
    device_id: str
    ip_address: str
    destination_id: str
    country: str


def generate_id(prefix: str, number: int) -> str:
    """Generate a simple deterministic ID."""
    return f"{prefix}_{number:06d}"


def generate_simulated_users(
    number_of_users: int,
    seed: int = 42
) -> list[SimulatedUser]:
    """
    Generate a population of simulated OTP users.
    """

    random.seed(seed)

    countries = [
        "US",
        "CA",
        "GB",
        "AU",
        "DE",
        "FR",
        "JP",
        "KR"
    ]

    users = []

    for i in range(1, number_of_users + 1):

        user = SimulatedUser(
            user_id=generate_id("user", i),
            device_id=generate_id("device", i),
            ip_address=f"192.0.2.{i % 254 + 1}",
            destination_id=generate_id("destination", i),
            country=random.choice(countries)
        )

        users.append(user)

    return users


def users_to_dicts(users: list[SimulatedUser]) -> list[dict]:
    """Convert simulated users into dictionaries."""
    return [asdict(user) for user in users]


if __name__ == "__main__":
    users = generate_simulated_users(
        number_of_users=10,
        seed=42
    )

    for user in users:
        print(user)