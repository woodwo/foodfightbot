import random
from app.models import Fighter
import copy
from typing import Tuple


def fight(fighter: Fighter, opponents: list[Fighter]) -> Tuple[Fighter, Fighter]:
    """Simulate a fight between a fighter and a random opponent."""

    opponents_copy = copy.deepcopy(opponents)

    try:
        opponents_copy.remove(fighter)
    except ValueError:
        pass

    opponent = random.choice(opponents_copy)

    return random.choice([fighter, opponent]), opponent

def create_fighter(name, icon, attack_power, description):
    """Used by unit tests"""
    fighter = Fighter()
    fighter.name = name
    fighter.icon = icon
    fighter.attack_power = attack_power
    fighter.description = description
    return fighter