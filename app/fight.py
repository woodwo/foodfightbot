import random
from app.models import Fighter
import copy
from typing import Tuple


def fight(fighter: Fighter, opponents: list[Fighter]) -> Tuple[Fighter, Fighter]:
    """Simulate a fight between a fighter and a random opponent."""
    # TODO do it in place maybe? too much copying
    opponents_copy = copy.deepcopy(opponents)
    opponents_copy = [f for f in opponents_copy if f.name != fighter.name]

    opponent = random.choice(opponents_copy)
    weights = [fighter.attack_power, opponent.attack_power]

    # TODO some tests for winner == fighter?
    # TODO some tests for weights
    return random.choices([fighter, opponent], weights, k=1)[0], opponent


def create_fighter(name, icon, attack_power, description):
    """Used by unit tests"""
    fighter = Fighter()
    fighter.name = name
    fighter.icon = icon
    fighter.attack_power = attack_power
    fighter.description = description
    return fighter
