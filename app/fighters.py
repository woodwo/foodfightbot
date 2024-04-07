import dataclasses


@dataclasses.dataclass
class Fighter:
    icon: str
    attack_power: int
    description: str


dumpling = Fighter(
    "🥟",
    19,
    "One dumpling will always turn into two dumplings. Two dumplings will turn into four. Call your dumpling friends to surround the enemy!",
)

kebab = Fighter(
    "🥙",
    14,
    "Feed your enemies some kebab! Oops, it looks like your kebab was made out of rotten meat! What did you expect from streetfood?",
)

nuggets = Fighter(
    "🍗",
    22,
    "Nuggets are the best choice for a quick meal. They are also the best choice for a quick fight!",
)

pizza = Fighter(
    "🍕",
    16,
    "This pizza sure has a lot of cheese! It looks like the enemy can't move... The cheese blocked him! Get your enemy stuck in cheese!",
)

toblerone = Fighter(
    "🍫",
    13,
    "Mmmm, what a delicious toblerone! The enemy seems distracted, he is busy eating toblerone..! Attack now!",
)

ramen = Fighter(
    "🍜",
    20,
    "Tie up your enemy with noodles and dip him in broth! This delicious ramen is unfortunately very aggressive",
)

fighters = [dumpling, kebab, nuggets, pizza, toblerone, ramen]