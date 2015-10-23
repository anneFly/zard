import json
import time

from . import card
from .player import init_players
from .turn import Turn
from .score import Score
from .exceptions import GameException


LEVELS = {
    3: 20,
    4: 15,
    5: 12,
    6: 10,
}

# GAME_STATES:
#     'WAITING_FOR_PLAYERS',
#     'STARTED',
#     'GUESSING',
#     'PLAYING',
#     'END',


class Game:
    def __init__(self, name, size):
        self.id = str(str(time.time()) + name).replace('.', '').replace(' ', '_')
        self.name = name
        self.size = size
        self.users = []

        self.initialize()

    def initialize(self):
        self.level = 1
        self.trump = None
        self.deck = card.generate_deck()
        self.players = []
        self.active_player = None
        self.turn = None
        self.last_winner = None
        self.score = Score()
        self.state = 'WAITING_FOR_PLAYERS'

    @property
    def num_players(self):
        return len(self.players)

    def add_user(self, user):
        self.users.append(user)
        if len(self.users) == self.size:
            self.start_game()

    def remove_user(self, user):
        idx = self.users.index(user)
        self.users.pop(idx)
        self.cancel_game()

    def send_state(self):
        for player in self.players:
            player.user.send(
                self.serialize(player)
            )

    def starters(self, start_idx):
        for p in self.players[start_idx:]:
            yield p
        for p in self.players[:start_idx]:
            yield p

    def give_cards(self):
        self.deck = card.generate_deck()
        for p in self.players:
            p.hand = []
            for i in range(self.level):
                card_ = self.deck.pop()
                card_.owner = p
                p.hand.append(card_)

        self.trump = self.deck.pop() if self.deck else None

    def get_start_index(self):
        return (self.level - 1) % self.num_players

    def get_turn_starter(self):
        if self.last_winner is not None:
            return self.players.index(self.last_winner)
        return self.get_start_index()

    def start_game(self):
        self.state = 'STARTED'
        self.players = init_players(self.users)
        self.start_level()

    def start_level(self):
        self.send_state()
        self.score.reset_round_score()
        self.give_cards()

        self.send_state()

        self.ordered_players = self.starters(self.get_start_index())
        self.start_guessing()

    def start_guessing(self):
        self.state = 'GUESSING'
        self.active_player = next(self.ordered_players)
        self.send_state()

    def on_guess(self, user, guess):
        if not self.state == 'GUESSING':
            raise GameException('Not the time to guess.')

        if self.active_player.user == user:
            self.score.guess_tricks(self.active_player, guess)
            try:
                self.active_player = next(self.ordered_players)
                self.send_state()
            except StopIteration:
                self.start_round()
        else:
            raise GameException('It\'s not your turn to guess.')

    def start_round(self):
        self.state = 'PLAYING'
        self.last_winner = None
        self.turns_to_play = self.level
        self.start_turn()

    def start_turn(self):
        self.turn = Turn()
        self.ordered_players = self.starters(self.get_turn_starter())
        self.active_player = next(self.ordered_players)
        self.send_state()

    def on_play_card(self, user, card_id):
        if not self.state == 'PLAYING':
            raise GameException('Not the time to play.')

        if self.active_player.user == user:
            card = self.active_player.play_card(card_id)
            can_serve = self.active_player.can_serve(self.turn.get_serving_color())

            # zards and nerds can always be played
            if card.value in ['Z', 'N'] or not can_serve:
                self.turn.pile.append(card)
                self.next_player()

            elif can_serve:
                if card.color == self.turn.get_serving_color():
                    self.turn.pile.append(card)
                    self.next_player()
                else:
                    # cannot play this card
                    self.active_player.hand.insert(card.hand_idx, card)
                    raise GameException('You cannot play this card.')
        else:
            raise GameException('It\'s not your turn.')

        self.send_state()

    def next_player(self):
        try:
            self.active_player = next(self.ordered_players)
            self.send_state()
        except StopIteration:
            self.end_turn()

    def end_turn(self):
        self.last_winner = self.turn.winner(self.trump.color)
        self.score.trick_counter[self.last_winner] += 1
        self.send_state()
        self.turns_to_play -= 1
        if self.turns_to_play == 0:
            self.score.count_points(self.players, self.score.guesses,
                                    self.score.trick_counter)
            self.send_state()
            self.next_level()
        else:
            self.start_turn()

    def next_level(self):
        if self.level == LEVELS[self.num_players]:
            self.finish_game()
        else:
            self.level += 1
            self.start_level()

    def finish_game(self):
        self.state = 'END'
        self.send_state()

    def cancel_game(self):
        self.initialize()

    def serialize(self, player):
        return json.dumps([
            'gameState',
            {
                'state': self.state,
                'level': self.level,
                'maxLevel': LEVELS[self.num_players],
                'players': [p.name for p in self.players],
                'trump': self.trump.id if self.trump else None,
                'activePlayer': self.active_player.name if self.active_player else None,
                'pile': [c.id for c in self.turn.pile] if self.turn else [],
                'lastWinner': self.last_winner.name if self.last_winner else None,
                'score': {p.name: score for p, score in self.score.score.items()},
                'tricks': {p.name: tricks for p, tricks in self.score.tricks.items()},
                'guesses': {p.name: guess for p, guess in self.score.guesses.items()},
                'hand': [c.id for c in player.hand],
            },
        ])
