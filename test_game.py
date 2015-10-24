import json
from unittest import mock

from zard import GameConnection, games


class MockInfo:
    ip = '123:456:78:90'


class MockConnection(GameConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = []

    def send(self, msg):
        entry = '{} {}'.format(self.name, msg)
        self.log.append(entry)

    def broadcast(self, recipients, msg):
        names = ', '.join([u.name for u in recipients])
        entry = '{} {}'.format(names, msg)
        self.log.append(entry)

    @property
    def last_log(self):
        try:
            return self.log[-1]
        except IndexError:
            return None


connection0 = MockConnection(mock.Mock())
connection1 = MockConnection(mock.Mock())
connection2 = MockConnection(mock.Mock())

connection0.on_open(MockInfo())
connection1.on_open(MockInfo())
connection2.on_open(MockInfo())

connection0.on_message(json.dumps(['rename', {'name': 'Player0'}]))
connection1.on_message(json.dumps(['rename', {'name': 'Player1'}]))
connection2.on_message(json.dumps(['rename', {'name': 'Player2'}]))

connection0.on_message(json.dumps(['createGame', {'name': 'my game', 'size': 3}]))
assert len(games) == 1
game_id = list(games.keys())[0]
gg = games[game_id]
connection1.on_message(json.dumps(['joinGame', {'id': game_id}]))
connection2.on_message(json.dumps(['joinGame', {'id': game_id}]))

assert len(gg.players) == 3
assert gg.level == 1
assert gg.state == 'GUESSING'
assert len(gg.players[0].hand) == 1
assert gg.trump is not None

gg.players[0].hand[0].color = 'red'
gg.players[0].hand[0].value = 2
gg.players[0].hand[0].id = '2r'
gg.players[1].hand[0].color = 'blue'
gg.players[1].hand[0].value = 13
gg.players[1].hand[0].id = '13b'
gg.players[2].hand[0].color = 'red'
gg.players[2].hand[0].value = 7
gg.players[2].hand[0].id = '7r'
gg.trump.color = 'green'
gg.trump.value = 1
gg.trump.id = '1g'

assert gg.active_player == gg.players[0]
connection0.on_message(json.dumps(['guess', {'guess': 0}]))
assert gg.score.guesses[gg.players[0]] == 0

assert gg.active_player == gg.players[1]
connection1.on_message(json.dumps(['guess', {'guess': 1}]))
assert gg.score.guesses[gg.players[1]] == 1

assert gg.active_player == gg.players[2]
connection2.on_message(json.dumps(['guess', {'guess': 1}]))
assert gg.score.guesses[gg.players[2]] == 1

assert gg.last_winner is None
assert gg.turns_to_play == 1


assert gg.active_player == gg.players[0]
connection0.on_message(json.dumps(['play', {'card': '2r'}]))
assert gg.turn.pile[-1].value == 2
assert gg.turn.pile[-1].color == 'red'
assert gg.turn.pile[-1].owner == gg.players[0]

assert gg.turn.get_serving_color() == 'red'

assert gg.active_player == gg.players[1]
connection1.on_message(json.dumps(['play', {'card': '13b'}]))
assert gg.turn.pile[-1].value == 13
assert gg.turn.pile[-1].color == 'blue'
assert gg.turn.pile[-1].owner == gg.players[1]

assert gg.active_player == gg.players[2]
connection2.on_message(json.dumps(['play', {'card': '7r'}]))
assert gg.turn.pile[-1].value == 7
assert gg.turn.pile[-1].color == 'red'
assert gg.turn.pile[-1].owner == gg.players[2]


assert gg.score.score[gg.players[0]] == 20
assert gg.score.score[gg.players[1]] == -10
assert gg.score.score[gg.players[2]] == 30

# second round ####

assert gg.level == 2
assert gg.state == 'GUESSING'
assert len(gg.players[0].hand) == 2
assert gg.trump is not None

gg.players[0].hand[0].color = 'yellow'
gg.players[0].hand[0].value = 'Z'
gg.players[0].hand[0].id = 'Zy'
gg.players[0].hand[1].color = 'blue'
gg.players[0].hand[1].value = 'N'
gg.players[0].hand[1].id = 'Nb'
gg.players[1].hand[0].color = 'blue'
gg.players[1].hand[0].value = 13
gg.players[1].hand[0].id = '13b'
gg.players[1].hand[1].color = 'yellow'
gg.players[1].hand[1].value = 13
gg.players[1].hand[1].id = '13y'
gg.players[2].hand[0].color = 'red'
gg.players[2].hand[0].value = 7
gg.players[2].hand[0].id = '7r'
gg.players[2].hand[1].color = 'blue'
gg.players[2].hand[1].value = 3
gg.players[2].hand[1].id = '3b'
gg.trump.color = 'red'
gg.trump.value = 1
gg.trump.id = '1r'

assert gg.active_player == gg.players[1]
connection1.on_message(json.dumps(['guess', {'guess': 2}]))
assert gg.score.guesses[gg.players[1]] == 2

assert gg.active_player == gg.players[2]
connection2.on_message(json.dumps(['guess', {'guess': 2}]))
assert gg.score.guesses[gg.players[2]] == 2

assert gg.active_player == gg.players[0]
connection0.on_message(json.dumps(['guess', {'guess': 1}]))
assert gg.score.guesses[gg.players[0]] == 1


assert gg.last_winner is None
assert gg.get_start_index() == 1
assert gg.turns_to_play == 2

assert gg.active_player == gg.players[1]
connection1.on_message(json.dumps(['play', {'card': '13b'}]))

assert gg.turn.get_serving_color() == 'blue'

# try to play card that is not on the hand
assert gg.active_player == gg.players[2]
connection2.on_message(json.dumps(['play', {'card': '3r'}]))
assert 'You don\'t have this card on your hand.' in connection2.last_log

# try to play trump even though player can serve
assert gg.active_player == gg.players[2]
connection2.on_message(json.dumps(['play', {'card': '7r'}]))
assert 'You cannot play this card.' in connection2.last_log

# finally play a correct card
assert gg.active_player == gg.players[2]
connection2.on_message(json.dumps(['play', {'card': '3b'}]))

assert gg.active_player == gg.players[0]
connection0.on_message(json.dumps(['play', {'card': 'Zy'}]))

assert gg.score.trick_counter[gg.players[0]] == 1
assert gg.score.trick_counter[gg.players[1]] == 0
assert gg.score.trick_counter[gg.players[2]] == 0

assert gg.last_winner == gg.players[0]
assert gg.get_turn_starter() == 0
assert gg.turns_to_play == 1

assert gg.active_player == gg.players[0]
connection0.on_message(json.dumps(['play', {'card': 'Nb'}]))

assert gg.turn.get_serving_color() is None

assert gg.active_player == gg.players[1]
connection1.on_message(json.dumps(['play', {'card': '13y'}]))

assert gg.turn.get_serving_color() == 'yellow'

assert gg.active_player == gg.players[2]
connection2.on_message(json.dumps(['play', {'card': '7r'}]))


assert gg.score.score[gg.players[0]] == 50
assert gg.score.score[gg.players[1]] == -30
assert gg.score.score[gg.players[2]] == 20


# third round ####

assert gg.level == 3
assert gg.state == 'GUESSING'
assert len(gg.players[0].hand) == 3
assert gg.trump is not None

gg.players[0].hand[0].color = 'yellow'
gg.players[0].hand[0].value = 'N'
gg.players[0].hand[0].id = 'Ny'
gg.players[0].hand[1].color = 'blue'
gg.players[0].hand[1].value = 'N'
gg.players[0].hand[1].id = 'Nb'
gg.players[0].hand[2].color = 'blue'
gg.players[0].hand[2].value = 'Z'
gg.players[0].hand[2].id = 'Zb'
gg.players[1].hand[0].color = 'green'
gg.players[1].hand[0].value = 'N'
gg.players[1].hand[0].id = 'Ng'
gg.players[1].hand[1].color = 'yellow'
gg.players[1].hand[1].value = 'Z'
gg.players[1].hand[1].id = 'Zy'
gg.players[1].hand[2].color = 'red'
gg.players[1].hand[2].value = 6
gg.players[1].hand[2].id = '6r'
gg.players[2].hand[0].color = 'red'
gg.players[2].hand[0].value = 'N'
gg.players[2].hand[0].id = 'Nr'
gg.players[2].hand[1].color = 'red'
gg.players[2].hand[1].value = 'Z'
gg.players[2].hand[1].id = 'Zr'
gg.players[2].hand[2].color = 'yellow'
gg.players[2].hand[2].value = 13
gg.players[2].hand[2].id = '13y'
# test zard as trump --> no trump color
gg.trump.color = 'green'
gg.trump.value = 'Z'
gg.trump.id = 'Zg'

assert gg.active_player == gg.players[2]
connection2.on_message(json.dumps(['guess', {'guess': 2}]))
assert gg.score.guesses[gg.players[2]] == 2

assert gg.active_player == gg.players[0]
connection0.on_message(json.dumps(['guess', {'guess': 2}]))
assert gg.score.guesses[gg.players[0]] == 2

assert gg.active_player == gg.players[1]
connection1.on_message(json.dumps(['guess', {'guess': 2}]))
assert gg.score.guesses[gg.players[1]] == 2


assert gg.last_winner is None
assert gg.get_start_index() == 2
assert gg.turns_to_play == 3

# test only nerds
assert gg.active_player == gg.players[2]
connection2.on_message(json.dumps(['play', {'card': 'Nr'}]))

assert gg.turn.get_serving_color() is None

assert gg.active_player == gg.players[0]
connection0.on_message(json.dumps(['play', {'card': 'Ny'}]))

assert gg.turn.get_serving_color() is None

assert gg.active_player == gg.players[1]
connection1.on_message(json.dumps(['play', {'card': 'Ng'}]))

assert gg.score.trick_counter[gg.players[0]] == 0
assert gg.score.trick_counter[gg.players[1]] == 0
assert gg.score.trick_counter[gg.players[2]] == 1

assert gg.last_winner == gg.players[2]
assert gg.get_turn_starter() == 2
assert gg.turns_to_play == 2

# test only zards
assert gg.active_player == gg.players[2]
connection2.on_message(json.dumps(['play', {'card': 'Zr'}]))

assert gg.turn.get_serving_color() is None

assert gg.active_player == gg.players[0]
connection0.on_message(json.dumps(['play', {'card': 'Zb'}]))

assert gg.turn.get_serving_color() is None

assert gg.active_player == gg.players[1]
connection1.on_message(json.dumps(['play', {'card': 'Zy'}]))

assert gg.score.trick_counter[gg.players[0]] == 0
assert gg.score.trick_counter[gg.players[1]] == 0
assert gg.score.trick_counter[gg.players[2]] == 2

assert gg.last_winner == gg.players[2]
assert gg.get_turn_starter() == 2
assert gg.turns_to_play == 1


assert gg.active_player == gg.players[2]
connection2.on_message(json.dumps(['play', {'card': '13y'}]))

assert gg.turn.get_serving_color() == 'yellow'

assert gg.active_player == gg.players[0]
connection0.on_message(json.dumps(['play', {'card': 'Nb'}]))

assert gg.turn.get_serving_color() == 'yellow'

assert gg.active_player == gg.players[1]
connection1.on_message(json.dumps(['play', {'card': '6r'}]))


assert gg.score.score[gg.players[0]] == 30
assert gg.score.score[gg.players[1]] == -50
assert gg.score.score[gg.players[2]] == 10

print('All tests passed!')
