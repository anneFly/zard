from collections import Counter


class Score:
    def __init__(self):
        self.score = Counter()
        self.guesses = {}
        self.tricks = Counter()

    def guess_tricks(self, player, guess):
        self.guesses[player] = guess

    def reset_round_score(self):
        self.trick_counter = Counter()
        self.guesses = {}

    def count_points(self, players, guesses, tricks):
        for p in players:
            diff = guesses[p] - tricks[p]
            if diff == 0:
                self.score[p] += (20 + tricks[p] * 10)
            else:
                self.score[p] -= abs(diff * 10)
