import dataclasses


@dataclasses.dataclass
class Fighter:
    name: str
    icon: str
    attack_power: int
    description: str

    def __str__(self):
        return f"{self.name} [{self.icon}] attack_power={self.attack_power}\n\n{self.description}\n---"


dumpling = Fighter(
    "Dumpling",
    "🥟",
    19,
    "One dumpling will always turn into two dumplings. Two dumplings will turn into four. Call your dumpling friends to surround the enemy!",
)

kebab = Fighter(
    "Kebab",
    "🥙",
    14,
    "Feed your enemies some kebab! Oops, it looks like your kebab was made out of rotten meat! What did you expect from streetfood?",
)

nuggets = Fighter(
    "Nuggets",
    "🍗",
    22,
    "Nuggets are the best choice for a quick meal. They are also the best choice for a quick fight!",
)

pizza = Fighter(
    "Pizza",
    "🍕",
    16,
    "This pizza sure has a lot of cheese! It looks like the enemy can't move... The cheese blocked him! Get your enemy stuck in cheese!",
)

toblerone = Fighter(
    "Toblerone",
    "🍫",
    13,
    "Mmmm, what a delicious toblerone! The enemy seems distracted, he is busy eating toblerone..! Attack now!",
)

ramen = Fighter(
    "Ramen",
    "🍜",
    20,
    "Tie up your enemy with noodles and dip him in broth! This delicious ramen is unfortunately very aggressive",
)


class MoreThanOneFighterException(Exception):
    def __init__(self, message="More than one fighter was chosen."):
        self.message = message
        super().__init__(self.message)


class FighterNonFoundException(Exception):
    pass


default_fighters = [dumpling, kebab, nuggets, pizza, toblerone, ramen]  # TODO set


def select_fighters(message: str, fighters: list[Fighter]) -> Fighter:
    message_words = set(message.lower().split())

    fighters_dict = {fighter.name.lower(): fighter for fighter in fighters}
    fighter_names = set(fighters_dict.keys())

    intersection = fighter_names.intersection(message_words)
    if len(intersection) == 1:
        return fighters_dict[intersection.pop()]
    if len(intersection) > 1:
        raise MoreThanOneFighterException(", ".join(intersection))
    else:
        raise FighterNonFoundException
