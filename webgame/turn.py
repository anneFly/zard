class Turn:
    def __init__(self):
        self.pile = []
        self.played = set()

    def get_serving_color(self):
        serving_color = None
        for card in self.pile:
            if card.value in ['Z', 'N']:
                continue
            serving_color = card.color
            break

        return serving_color

    def highest_card(self, color):
        def highest_value(c):
            if c.color == color and c.value != 'N':
                return c.value
            else:
                return 0

        return max(self.pile, key=highest_value)

    def winner(self, trump_color):
        # if Zard in pile --> first zard wins
        for played_card in self.pile:
            if played_card.value == 'Z':
                return played_card.owner

        # if only nerds --> don't get serving color, return first nerd
        if all(card.value == 'N' for card in self.pile):
            return self.pile[0].owner

        # has a card in trump color been played?
        if trump_color is not None:
            if any(card.value != 'N' and card.color == trump_color for card in self.pile):
                # if someone played a card in trump color
                highest_card = self.highest_card(trump_color)
                return highest_card.owner

        # if there was no trump color or no trump color was played
        highest_card = self.highest_card(self.get_serving_color())
        return highest_card.owner
