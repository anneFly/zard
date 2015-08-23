import json

from . import card
from . import player
from . import turn as turn_module
from . import score as score_module
from .exceptions import GameException


class Game:
    def __init__(self, shuffle_deck=True):
        self.shuffle_deck = shuffle_deck

        self.users = []
        self.level = 1
        self.starter = 0
        self.trump = None
        self.pile = []
        self.deck = card.generate_deck(shuffle_deck=shuffle_deck)
        self.players = []
        self.score = score_module.Score()
        self.state = 'default'

    level_map = {
        3: 20,
        4: 15,
        5: 12,
        6: 10,
    }

    @property
    def num_players(self):
        return len(self.users)

    def add_user(self, user, name):
        self.users.append((user, name,))
        user.broadcast([user], json.dumps(['message', 'You are {}.'.format(name)]))

    def give_cards(self):
        self.deck = card.generate_deck(shuffle_deck=self.shuffle_deck)
        for p in self.players:
            p.hand = []
            for i in range(self.level):
                p.hand.append(self.deck.pop())

        self.trump = self.deck.pop() if self.deck else None

    def get_start_index(self):
        return (self.level - 1) % self.num_players

    def next_level(self):
        if self.level == self.level_map[self.num_players]:
            self.finish_game()
        else:
            self.level += 1
            self.start_idx = self.get_start_index()
            self.start_level()

    def start(self):
        self.players = player.init_players(self.users)
        self.start_idx = self.get_start_index()
        self.start_level()

    def start_level(self):
        self.users[0][0].broadcast(
            [u[0] for u in self.users],
            json.dumps(['message', 'starting level {}'.format(self.level)])
        )
        self.give_cards()
        self.users[0][0].broadcast(
            [u[0] for u in self.users],
            json.dumps(['trump', '{}'.format(self.trump)])
        )
        for p in self.players:
            p.user.broadcast([p.user], json.dumps(['hand', p.get_hand()]))

        self.starting_players = self.starters(self.start_idx)
        self.start_guessing()

    def notify_player_to_guess(self):
        self.active_player.user.broadcast(
            [self.active_player.user],
            json.dumps(['message', 'it\'s your turn. Make your guess.'])
        )

    def notify_player_to_play(self):
        self.active_player.user.broadcast(
            [self.active_player.user],
            json.dumps(['message', 'it\'s your turn. Play a card.'])
        )

    def start_guessing(self):
        self.state = 'guessing'
        self.tricks = score_module.Tricks()
        # self.starter
        self.active_player = next(self.starting_players)
        self.notify_player_to_guess()

    def on_guess(self, user, guess):
        if not self.state == 'guessing':
            raise GameException('Not the time to guess.')

        if self.active_player.user == user:
            self.tricks.guess_tricks(self.active_player, guess)
            try:
                self.active_player = next(self.starting_players)
                self.notify_player_to_guess()
            except:
                self.start_round()
        else:
            raise GameException('It\'s not your turn to guess.')

    def start_round(self):
        self.last_winner = None
        self.turns_to_play = self.level
        self.start_turn()

    def start_turn(self):
        self.state = 'turn'
        self.turn = turn_module.Turn()
        self.turn.starter = self.last_winner or self.start_idx
        self.starting_players = self.starters(self.turn.starter)
        self.active_player = next(self.starting_players)
        self.notify_player_to_play()

    def end_turn(self):
        trick_winner = self.turn.winner(self.trump.color)
        self.tricks.trick_counter[trick_winner.name] += 1
        for idx, p in enumerate(self.players):
            if p.name == trick_winner.name:
                self.last_winner = idx
                break

        self.active_player.user.broadcast(
            [u[0] for u in self.users],
            json.dumps(['message', 'The trick goes to {}'.format(trick_winner.name)])
        )
        self.turns_to_play -= 1
        if self.turns_to_play == 0:
            self.score.count_points(self.players, self.tricks.guesses,
                                    self.tricks.trick_counter)
            self.active_player.user.broadcast(
                [u[0] for u in self.users],
                json.dumps(['message', 'score: {}'.format(str(self.score.score))])
            )
            self.next_level()
        else:
            self.start_turn()

    def next_player(self):
        if self.turn.played == 0:
            self.turn.set_serving_color()
        self.turn.played.add(self.active_player.name)
        try:
            self.active_player = next(self.starting_players)
            self.notify_player_to_play()
        except:
            self.end_turn()

    def on_play_card(self, user, card_id):
        if not self.state == 'turn':
            raise GameException('Not the time to play.')

        if self.active_player.user == user:
            card = self.active_player.play_card(card_id)
            if not self.active_player.can_serve(self.turn.serving_color):
                self.turn.pile.append([self.active_player, card])
                self.next_player()
            else:
                if card.color == self.turn.serving_color or \
                   self.turn.serving_color is None or \
                   card.value in ['Z', 'N']:
                    self.turn.pile.append([self.active_player, card])
                    self.next_player()
                else:
                    # cannot play this card
                    self.active_player.hand.insert(card.hand_idx, card)
                    card = None
                    self.active_player.user.broadcast(
                        [self.active_player.user],
                        json.dumps(['message', 'You cannot play this card.'])
                    )
        else:
            raise GameException('It\'s not your turn.')

    def starters(self, start_idx):
        for p in self.players[start_idx:]:
            yield p
        for p in self.players[:start_idx]:
            yield p

    def finish_game(self):
        self.state = 'end'
        self.users[0][0].broadcast(
            [u[0] for u in self.users],
            json.dumps(['finalscore', str(self.score.score)])
        )
