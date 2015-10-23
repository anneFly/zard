import json
from unittest import mock

from zard import GameConnection, games, users


class MockInfo:
    ip = '123:456:78:90'


class MockConnection(GameConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = []

    def send(self, msg):
        entry = '{} {}'.format(self.name, msg)
        self.log.append(entry)
        print(entry)

    def broadcast(self, recipients, msg):
        names = ', '.join([u.name for u in recipients])
        entry = '{} {}'.format(names, msg)
        self.log.append(entry)
        print(entry)

    @property
    def last_log(self):
        try:
            return self.log[-1]
        except IndexError:
            return None


connection0 = MockConnection(mock.Mock())
connection1 = MockConnection(mock.Mock())
connection2 = MockConnection(mock.Mock())

assert len(games.items()) == 0
assert len(users) == 0

connection0.on_open(MockInfo())
assert len(users) == 1
assert '"numUsers": 1' in connection0.last_log

connection1.on_open(MockInfo())
assert '"numUsers": 2' in connection1.last_log

connection2.on_open(MockInfo())
assert '"numUsers": 3' in connection2.last_log

# rename
connection0.on_message(json.dumps(['rename']))
assert 'You must provide a name.' in connection0.last_log

connection0.on_message(json.dumps(['rename', 'Player0']))
assert 'Player0' in connection0.last_log
connection1.on_message(json.dumps(['rename', 'Player1']))
connection2.on_message(json.dumps(['rename', 'Player2']))

connection0.on_message(json.dumps(['createGame', 'xx']))
assert 'You must provide a name and a size for your game.' in connection0.last_log

connection0.on_message(json.dumps(['createGame', 'xx', 2]))
assert 'The game name is too short (min 3 characters).' in connection0.last_log

connection0.on_message(json.dumps(['createGame', 'foo game', 2]))
assert 'The game size must be between 3 and 6.' in connection0.last_log

connection0.on_message(json.dumps(['createGame', 'foo game', 3]))
assert len(games.items()) == 1
assert connection0.game
assert '"size": 3' in connection0.last_log
assert '"status": "WAITING_FOR_PLAYERS"' in connection0.last_log
assert '"users": ["Player0"]' in connection0.last_log
assert 'foo game' in connection0.last_log

game_id = connection0.game.id

connection0.on_message(json.dumps(['joinGame', game_id]))
assert 'You already joined a game.' in connection0.last_log

connection1.on_message(json.dumps(['joinGame', 'test']))
assert 'Unable to find the game.' in connection1.last_log

connection1.on_message(json.dumps(['joinGame', game_id]))
assert len(games.items()) == 1
assert connection1.game
assert '"size": 3' in connection1.last_log
assert '"status": "WAITING_FOR_PLAYERS"' in connection1.last_log
assert '"users": ["Player0", "Player1"]' in connection1.last_log
assert 'foo game' in connection1.last_log

connection2.on_message(json.dumps(['joinGame', game_id]))

assert connection2.game
assert '"size": 3' in connection2.last_log
assert '"status": "GUESSING"' in connection2.last_log
assert '"users": ["Player0", "Player1", "Player2"]' in connection2.last_log
assert 'foo game' in connection2.last_log

connection2.on_message(json.dumps(['leaveGame']))
assert connection2.game is None
assert '"status": "WAITING_FOR_PLAYERS"' in connection2.last_log
assert '"users": ["Player0", "Player1"]' in connection2.last_log

connection1.on_message(json.dumps(['leaveGame']))
assert connection1.game is None
assert len(games.items()) == 1

connection0.on_message(json.dumps(['leaveGame']))
assert connection0.game is None
assert len(games.items()) == 0
