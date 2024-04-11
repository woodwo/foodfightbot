import random
from app.models import Fighter


def hire(candidates: list[Fighter]) -> Fighter:
    """Simulate a new hire."""
    return random.choice(candidates)
