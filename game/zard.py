import card
import player
import turn as turn_module
import score as score_module


class Game:
    def __init__(self):
        self.num_players = self.set_players()
        self.player_names = self.set_player_names()
        self.level = 1
        self.starter = 0
        self.trump = None
        self.pile = []
        self.deck = card.generate_deck()
        self.players = player.init_players(self.player_names)
        self.score = score_module.Score()

    level_map = {
        3: 20,
        4: 15,
        5: 12,
        6: 10,
    }

    def set_players(self):
        player_num_input = None
        while player_num_input is None:
            player_num_input = input("How many players? -->")
            if not player_num_input in ['3', '4', '5', '6']:
                player_num_input = None
                print("please enter a number between 3 and 6")

        return int(player_num_input)

    def set_player_names(self):
        player_names = []
        for i in range(self.num_players):
            player_names.append(input("player {}: please enter your name -->".format(i+1)))
        return player_names

    def give_cards(self):
        self.deck = card.generate_deck()
        for p in self.players:
            p.hand = []
            for i in range(self.level):
                p.hand.append(self.deck.pop())

        self.trump = self.deck.pop() if self.deck else None

    def set_starter(self):
        return (self.level - 1) % self.num_players

    def next_level(self):
        self.level += 1
        self.starter = self.set_starter()
        print('**************\n next turn \n ****************')

    def play_level(self):
        print("Level {} - Trump color is {}".format(self.level, self.trump.col))
        tricks = score_module.Tricks()
        for p in self.start_at(self.players, self.starter):
            tricks.guess_tricks(p)
        last_winner = None
        for i in range(self.level):
            turn = turn_module.Turn()
            turn.starter = last_winner if not last_winner is None else self.starter
            for p in self.start_at(self.players, turn.starter):
                card = None
                turn.set_serve_color()
                while card is None:
                    card = p.play_card()
                    if not p.can_serve(turn.serving_color):
                        turn.pile.append([p.name, card])
                    else:
                        if turn.serving_color == card.col or turn.serving_color is None or card.val in ['Z', 'N']:
                            turn.pile.append([p.name, card])
                        else:
                            print("you cannot play this card")
                            p.hand.insert(card.hand_idx, card)
                            card = None
            trick_winner = turn.winner(self.trump.col)
            tricks.trick_counter[trick_winner] += 1
            for idx, p in enumerate(self.players):
                if p.name == trick_winner:
                    last_winner = idx
                    break
        self.score.count_points(self.players, tricks.guesses, tricks.trick_counter)
        print(self.score.score)

    def start_at(self, items, start_index):
        for item in items[start_index:]:
            yield item
        for item in items[:start_index]:
            yield item

    def main(self):
        for level in range(self.level_map[self.num_players]):
            self.give_cards()
            self.play_level()
            self.next_level()

        print("~~~~~~~~~~~\n End\n overall score: {}\n~~~~~~~~~~~".format(self.score.score))

print("~~~~~~~~~~~\n NEW GAME\n~~~~~~~~~~~")

new_game = Game()
new_game.main()
