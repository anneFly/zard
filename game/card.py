from random import shuffle


class Card:
    def __init__(self, color, value):
        self.col = color
        self.val = value

    def __repr__(self):
        return "{} {}".format(self.col, self.val)


def generate_deck():
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 'Z', 'N']
    colors = ['blue', 'yellow', 'green', 'red']
    deck = []
    for c in colors:
        for v in values:
            deck.append(Card(c, v))
    shuffle(deck)

    return deck
