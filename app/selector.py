from app.models import Fighter
from rapidfuzz import fuzz
import inflect

stem = inflect.engine()

def _stem_metaphone(word: str) -> str:
    w = stem.singular_noun(word) or word
    return w.lower()

class MoreThanOneFighterException(Exception):
    def __init__(self, message="More than one fighter was chosen."):
        self.message = message
        super().__init__(self.message)


class FighterNonFoundException(Exception):
    pass


def select_fighters(message: str, fighters: list[Fighter]) -> Fighter:
    message = "".join(ch for ch in message if ch.isalpha() or ch.isspace())
    message_words = [word.lower() for word in message.split()]
    
    matches = []
    for fighter in fighters:
        fighter_name = _stem_metaphone(fighter.name)
        for word in message_words:
            word = _stem_metaphone(word)
            score = fuzz.ratio(fighter_name, word)
            if score >= 75:  # threshold for vague matching
                matches.append(fighter)
                break
    
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        raise MoreThanOneFighterException(", ".join([f.name for f in matches]))
    else:
        raise FighterNonFoundException
