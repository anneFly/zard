class Turn:
    def __init__(self):
        self.pile = []
        self.serving_color = None

    def set_serve_color(self):
        if self.serving_color is None and len(self.pile) > 0:
            if self.pile[-1][1].val in ['Z', 'N']:
                self.serving_color = None
            else:
                self.serving_color = self.pile[-1][1].col

    def get_serve_color(self):
        serving_color = None
        i = 0
        while serving_color is None:
            if self.pile[i][1].val in ['Z', 'N']:
                i += 1
            else:
                serving_color = self.pile[i][1].col
                return serving_color

    def winner(self, trump_color):
        # if Zard in pile --> first zard wins
        for card in self.pile:
            if card[1].val == 'Z':
                print("A wizard was played")
                print("The trick goes to {}".format(card[0]))
                return card[0]

        # if only nerds --> don't get serving color, return first nerd
        for idx, card in enumerate(self.pile):
            if card[1].val == 'N' and idx == len(self.pile) - 1:
                print("only nerds were played")
                print("The trick goes to {}".format(card[0]))
                return card[0]
            if card[1].val != 'N':
                break

        # has a card in trump color been played?
        trump_played = False
        for card in self.pile:
            if card[1].col == trump_color and not card[1].val in ['Z', 'N'] :
                trump_played = True
                break

        # if there was no trump color or no trump color was played
        if trump_color is None or trump_played is False:
            serving_color = self.get_serve_color()
            highest_val = 0
            highest_card = self.pile[0]
            for card in self.pile:
                if not card[1].val in ['Z', 'N'] and card[1].col == serving_color and card[1].val > highest_val:
                    highest_val = card[1].val
                    highest_card = card

            print("The color to be served was {}".format(serving_color))
            print("The trick goes to {}".format(highest_card[0]))

            return highest_card[0]

        # if someone played a card in trump color
        highest_val = 0
        highest_card = self.pile[0]
        for card in self.pile:
            if not card[1].val in ['Z', 'N'] and card[1].col == trump_color and card[1].val > highest_val:
                highest_val = card[1].val
                highest_card = card

        print("Someone played trump")
        print("The trick goes to {}".format(highest_card[0]))

        return highest_card[0]
