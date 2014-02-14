class Player:
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.tricks = []

    def play_card(self):
        print("{}: {}".format(self.name, self.hand))
        card_idx = None

        while card_idx is None:
            card_idx = input("--> play a card: ")
            try:
                card_idx = int(card_idx)
                card = self.hand.pop(card_idx)
            except (TypeError, ValueError):
                card_idx = None
                print("wrong input")
            except IndexError:
                card_idx = None
                print("invalid card index")

        card.hand_idx = card_idx
        return card

    def can_serve(self, serving_color):
        if serving_color is None:
            return True

        for card in self.hand:
            if card.col == serving_color and not card.val in ["Z", "N"]:
                return True

        return False


def init_players(player_names):
    players = []
    for n in player_names:
        players.append(Player(n))

    return players
