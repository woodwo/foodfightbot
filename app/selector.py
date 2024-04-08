from app.models import Fighter
from fuzzy import DMetaphone

metaphone = DMetaphone()

class MoreThanOneFighterException(Exception):
    def __init__(self, message="More than one fighter was chosen."):
        self.message = message
        super().__init__(self.message)


class FighterNonFoundException(Exception):
    pass


def select_fighters(message: str, fighters: list[Fighter]) -> Fighter:
    message = ''.join(ch for ch in message if ch.isalpha() or ch.isspace())
    message_words = {metaphone(word)[0]: word for word in message.lower().split()}

    fighters_dict = {metaphone(fighter.name.lower())[0]: fighter for fighter in fighters}

    intersection = set(fighters_dict.keys()).intersection(set(message_words.keys()))
    if len(intersection) == 1:
        return fighters_dict[intersection.pop()]
    if len(intersection) > 1:
        human_words = [message_words[word] for word in intersection]
        raise MoreThanOneFighterException(", ".join(human_words))
    else:
        raise FighterNonFoundException
