import enum

class Suit(enum.Enum):
    SPADES = 1
    HEART = 2
    CLUB = 3
    DIAMOND = 4

for suit in Suit:
    print(suit.name)