import collections


class Tricks:
    def __init__(self):
        self.guesses = {}
        self.trick_counter = collections.defaultdict(int)

    def guess_tricks(self, player, guess):
        self.guesses[player.name] = int(guess)


class Score:
    def __init__(self):
        self.score = collections.defaultdict(int)

    def count_points(self, players, guesses, tricks):
        for p in players:
            diff = guesses[p.name] - tricks[p.name]
            if diff == 0:
                self.score[p.name] += 20
                self.score[p.name] += (tricks[p.name] * 10)
            else:
                self.score[p.name] -= abs(diff * 10)
