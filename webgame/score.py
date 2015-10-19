from collections import Counter


class Score:
    def __init__(self):
        self.score = Counter()
        self.guesses = {}
        self.tricks = Counter()

    def guess_tricks(self, player, guess):
        self.guesses[player.name] = int(guess)

    def reset_turn_score(self):
        self.trick_counter = Counter()
        self.guesses = {}

    def count_points(self, players, guesses, tricks):
        for p in players:
            diff = guesses[p.name] - tricks[p.name]
            if diff == 0:
                self.score[p.name] += (20 + tricks[p.name] * 10)
            else:
                self.score[p.name] -= abs(diff * 10)
