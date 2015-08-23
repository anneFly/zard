import zard


class MockConnection:
    broadcast_log = []

    def broadcast(self, to, msg):
        self.broadcast_log.append({
            'to': to,
            'msg': msg,
        })

gg = zard.game.Game(shuffle_deck=False)

connection1 = MockConnection()
connection2 = MockConnection()
connection3 = MockConnection()

gg.add_user(connection1, 'player1')
gg.add_user(connection2, 'player2')
gg.add_user(connection3, 'player3')

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
assert gg.turn.pile[-1][1].value == 2
assert gg.turn.pile[-1][1].color == 'red'

assert gg.turn.get_serving_color() == 'red'

assert gg.active_player == gg.players[1]
gg.on_play_card(gg.players[1].user, '13b')
assert gg.turn.pile[-1][1].value == 13
assert gg.turn.pile[-1][1].color == 'blue'

assert gg.active_player == gg.players[2]
gg.on_play_card(gg.players[2].user, '7r')
assert gg.turn.pile[-1][1].value == 7
assert gg.turn.pile[-1][1].color == 'red'


assert gg.score.score[gg.players[0].name] == 20
assert gg.score.score[gg.players[1].name] == -10
assert gg.score.score[gg.players[2].name] == 30

# second round ####

assert gg.level == 2
assert gg.state == 'guessing'
assert len(gg.players[0].hand) == 2
assert gg.trump is not None
