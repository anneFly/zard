class Turn:
    def __init__(self):
        self.pile = []
        self.serving_color = None
        self.played = set()

    def set_serving_color(self):
        if self.serving_color is None and len(self.pile) > 0:
            if self.pile[-1].value in ['Z', 'N']:
                self.serving_color = None
            else:
                self.serving_color = self.pile[-1].color

    def get_serving_color(self):
        serving_color = None
        i = 0
        while serving_color is None:
            if self.pile[i].value in ['Z', 'N']:
                i += 1
                if len(self.pile) == 1:
                    return serving_color
            else:
                serving_color = self.pile[i].color
                return serving_color

    def winner(self, trump_color):
        # if Zard in pile --> first zard wins
        for played_card in self.pile:
            if played_card.value == 'Z':
                return played_card.owner

        # if only nerds --> don't get serving color, return first nerd
        for idx, played_card in enumerate(self.pile):
            if played_card.value == 'N' and idx == len(self.pile) - 1:
                return played_card.owner
            if played_card.value != 'N':
                break

        # has a card in trump color been played?
        trump_played = False
        for played_card in self.pile:
            if played_card.value in ['Z', 'N']:
                continue

            if played_card.color == trump_color:
                trump_played = True
                break

        # if there was no trump color or no trump color was played
        if trump_color is None or trump_played is False:
            serving_color = self.get_serving_color()
            highest_value = 0
            highest_card = self.pile[0]
            for played_card in self.pile:
                if played_card.value not in ['Z', 'N'] \
                        and played_card.color == serving_color \
                        and played_card.value > highest_value:
                    highest_value = played_card.value
                    highest_card = played_card

            return highest_card.owner

        # if someone played a card in trump color
        highest_value = 0
        highest_card = self.pile[0]
        for played_card in self.pile:
            if played_card.value not in ['Z', 'N'] \
                    and played_card.color == trump_color \
                    and played_card.value > highest_value:
                highest_value = played_card.value
                highest_card = played_card

        return highest_card.owner
