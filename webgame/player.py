from .exceptions import GameException


class Player:
    def __init__(self, user, name):
        self.hand = []
        self.name = name
        self.tricks = []
        self.user = user

    def get_hand(self):
        return [c.id for c in self.hand]

    def play_card(self, card_id):
        if card_id not in self.get_hand():
            raise GameException('you don\'t have this card on your hand.')

        for idx, card in enumerate(self.hand):
            if card.id == card_id:
                self.hand.pop(idx)
                card.hand_idx = idx
                return card

    def can_serve(self, serving_color):
        if serving_color is None:
            return True

        for card in self.hand:
            if card.color == serving_color and card.value not in ["Z", "N"]:
                return True

        return False


def init_players(users):
    players = []
    for n in users:
        players.append(Player(n[0], n[1]))

    return players
