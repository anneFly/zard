from random import shuffle


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.id = '{}{}'.format(value, color[0])

    def __repr__(self):
        return '{} {}'.format(self.color, self.value)


def generate_deck(shuffle_deck=True):
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 'Z', 'N']
    colors = ['blue', 'yellow', 'green', 'red']
    deck = []
    for c in colors:
        for v in values:
            deck.append(Card(c, v))

    if shuffle_deck:
        shuffle(deck)

    return deck
