import random
from app.fighters import Fighter
import copy


def fight(fighter: Fighter, opponents: list[Fighter]) -> Fighter:
    """Simulate a fight between a fighter and a random opponent."""

    opponents_copy = copy.deepcopy(opponents)

    try:
        opponents_copy.remove(fighter)
    except ValueError:
        pass

    opponent = random.choice(opponents_copy)

    return random.choice([fighter, opponent])
