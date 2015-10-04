import zard


class MockConnection:
    broadcast_log = []

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')

    def broadcast(self, to, msg):
        print('{} {}'.format(to[0].name, msg))

gg = zard.game.Game(shuffle_deck=False)

connection1 = MockConnection(name='player0')
connection2 = MockConnection(name='player1')
connection3 = MockConnection(name='player2')

gg.add_user(connection1, 'player0')
gg.add_user(connection2, 'player1')
gg.add_user(connection3, 'player2')

assert len(gg.users) == 3

gg.start()

assert len(gg.players) == 3
assert gg.level == 1
assert gg.state == 'guessing'
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
gg.on_guess(gg.players[0].user, 0)
assert gg.tricks.guesses[gg.players[0].name] == 0

assert gg.active_player == gg.players[1]
gg.on_guess(gg.players[1].user, 1)
assert gg.tricks.guesses[gg.players[1].name] == 1

assert gg.active_player == gg.players[2]
gg.on_guess(gg.players[2].user, 1)
assert gg.tricks.guesses[gg.players[2].name] == 1

assert gg.last_winner is None
assert gg.turns_to_play == 1


assert gg.active_player == gg.players[0]
gg.on_play_card(gg.players[0].user, '2r')
assert gg.turn.pile[-1].value == 2
assert gg.turn.pile[-1].color == 'red'
assert gg.turn.pile[-1].owner == gg.players[0]

assert gg.turn.get_serving_color() == 'red'

assert gg.active_player == gg.players[1]
gg.on_play_card(gg.players[1].user, '13b')
assert gg.turn.pile[-1].value == 13
assert gg.turn.pile[-1].color == 'blue'
assert gg.turn.pile[-1].owner == gg.players[1]

assert gg.active_player == gg.players[2]
gg.on_play_card(gg.players[2].user, '7r')
assert gg.turn.pile[-1].value == 7
assert gg.turn.pile[-1].color == 'red'
assert gg.turn.pile[-1].owner == gg.players[2]


assert gg.score.score[gg.players[0].name] == 20
assert gg.score.score[gg.players[1].name] == -10
assert gg.score.score[gg.players[2].name] == 30

# second round ####

assert gg.level == 2
assert gg.state == 'guessing'
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
gg.players[2].hand[1].color = 'red'
gg.players[2].hand[1].value = 3
gg.players[2].hand[1].id = '3r'
gg.trump.color = 'red'
gg.trump.value = 1
gg.trump.id = '1r'

assert gg.active_player == gg.players[1]
gg.on_guess(gg.players[1].user, 2)
assert gg.tricks.guesses[gg.players[1].name] == 2

assert gg.active_player == gg.players[2]
gg.on_guess(gg.players[2].user, 2)
assert gg.tricks.guesses[gg.players[2].name] == 2

assert gg.active_player == gg.players[0]
gg.on_guess(gg.players[0].user, 1)
assert gg.tricks.guesses[gg.players[0].name] == 1


assert gg.last_winner is None
assert gg.start_idx == 1
assert gg.turns_to_play == 2

assert gg.active_player == gg.players[1]
gg.on_play_card(gg.players[1].user, '13b')

assert gg.turn.get_serving_color() == 'blue'

assert gg.active_player == gg.players[2]
gg.on_play_card(gg.players[2].user, '3r')

assert gg.active_player == gg.players[0]
gg.on_play_card(gg.players[0].user, 'Zy')

assert gg.tricks.trick_counter['player0'] == 1
assert gg.tricks.trick_counter['player1'] == 0
assert gg.tricks.trick_counter['player2'] == 0

assert gg.last_winner == 0
assert gg.turn.starter == 0
assert gg.turns_to_play == 1

assert gg.active_player == gg.players[0]
gg.on_play_card(gg.players[0].user, 'Nb')

assert gg.turn.get_serving_color() is None

assert gg.active_player == gg.players[1]
gg.on_play_card(gg.players[1].user, '13y')

assert gg.turn.get_serving_color() == 'yellow'

assert gg.active_player == gg.players[2]
gg.on_play_card(gg.players[2].user, '7r')


assert gg.score.score[gg.players[0].name] == 50
assert gg.score.score[gg.players[1].name] == -30
assert gg.score.score[gg.players[2].name] == 20
