import itertools
import random
import time

input_dict = {7: (0, 0), 8: (0, 1), 9: (0, 2),
              4: (1, 0), 5: (1, 1), 6: (1, 2),
              1: (2, 0), 2: (2, 1), 3: (2, 2)}

straight_two_comb = {(1, 4): 7, (1, 7): 4, (4, 7): 1,
                     (2, 5): 8, (2, 8): 5, (5, 8): 2,
                     (3, 6): 9, (3, 9): 6, (6, 9): 3,

                     (1, 2): 3, (1, 3): 2, (2, 3): 1,
                     (4, 5): 6, (4, 6): 5, (5, 6): 4,
                     (7, 8): 9, (7, 9): 8, (8, 9): 7,

                     (1, 5): 9, (1, 9): 5, (5, 9): 1,
                     (7, 5): 3, (7, 3): 5, (5, 3): 7}

corner_entry = [7, 9, 1, 3]
edge_entry = [8, 4, 6, 2]

columns = ((7, 4, 1), (8, 5, 2), (9, 6, 3))
rows = ((7, 8, 9), (4, 5, 6), (1, 2, 3))


class TicTacToe:
    def __init__(self):
        self.Board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        self.available_entry = [i for i in range(1, 10)]
        self.player = random.choice([1, 2])  # to decide who will play first
        self.move = 0  # count the moves to decide computer's move
        self.player_entry = []
        self.comp_entry = []
        self.corner_spots = [7, 9, 1, 3]
        self.edge_spots = [8, 4, 6, 2]


        if self.player == 1:
            self.comp_first_turn = False  # to decide comp moves based on comp's 1st/2nd turn
            print("Your turn first")
        else:
            self.comp_first_turn = True
            print("Computer will play first")

    def check_valid_move(self, key):
        if key in self.available_entry:
            return True

    def update_available_spots(self, entry):  # to use after every make move
        self.available_entry.remove(entry)
        if entry in self.edge_spots:
            self.edge_spots.remove(entry)
        if entry in self.corner_spots:
            self.corner_spots.remove(entry)

    def make_move(self, r, c):  # to mark selected spot on board by player/comp
        # if self.is_valid_move(r, c):
        self.Board[r][c] = self.player  # board array will be marked as 1 or 2 (player number)
        self.player = (self.player % 2) + 1  # toggle between player 1 and 2

    def check_winner(self):  # check any 3 consecutive spot are same
        for c in range(3):  # column
            if self.Board[0][c] == self.Board[1][c] == self.Board[2][c] != 0:
                return self.Board[0][c]

        for r in range(3):  # row
            if self.Board[r][0] == self.Board[r][1] == self.Board[r][2] != 0:
                return self.Board[r][0]

        if self.Board[0][0] == self.Board[1][1] == self.Board[2][2] != 0:  # diagonal (\)
            return self.Board[0][0]
        if self.Board[2][0] == self.Board[1][1] == self.Board[0][2] != 0:  # diagonal (/)
            return self.Board[2][0]

        if not self.available_entry:  # check no open spots then draw
            return 0
        return -1  # game is not over yet

    def win_chance(self, entry):  # Check (player/comp) who got 2 consecutive spots (Avoid_loss)
        alert_combination = {i for i in itertools.permutations(entry, 2)}
        for alert_set in alert_combination:
            if alert_set in straight_two_comb:
                [r, c] = input_dict[straight_two_comb[alert_set]]
                key = list(input_dict.keys())[list(input_dict.values()).index((r, c))]
                if key in self.available_entry:
                    return key
        else:
            return False

    def print_board(self):
        chars = ["_", "X", "O"]  # index of this correspond to player 1 and 2 symbols
        print()
        for r in range(3):
            for c in range(3):
                print(chars[self.Board[r][c]], end=' ')
            print()
        print()

    def smart_spot(self, player_entry):
        # avoid player's fork by choosing common corner spot (CCS) between player's 1st 2 entry
        common = []
        for i in range(len(self.player_entry)):
            r = [x for x in rows if self.player_entry[i] in x]
            c = [x for x in columns if self.player_entry[i] in x]

            common.append(r[0])
            common.append(c[0])

        common = list(itertools.chain(*common))
        common = [i for i in common if i not in (set(player_entry).union(set(edge_entry)))]
        if max(set(common), key=common.count) in self.available_entry:
            return max(set(common), key=common.count)

    def first_comp(self):  # comp algorithm when comp has first move
        if len(self.comp_entry) == 0:
            return random.choice(self.corner_spots)
        elif len(self.comp_entry) == 1:  # on comp 2nd move (game's 3rd)
            if list(self.player_entry)[-1] == 5:  # player choose center spot
                print("thinking...")
                time.sleep(2)
                key = {1: 9, 9: 1, 3: 7, 7: 3}[self.comp_entry[-1]]
                # comp choose opposite corner
            else:
                key = 5  # Comp choose center
            return key

    @property
    def second_comp(self):  # comp algorithm when comp has second move
        # when player's turn is First
        if self.win_chance(self.player_entry):
            return self.win_chance(self.player_entry)
        elif len(self.player_entry) == 1:
            if self.player_entry[0] == 5:
                return random.choice(self.corner_spots)
            else:  # self.player_entry[-1] in (corner_entry or edge_entry):
                return 5
        elif len(self.player_entry) == 2:
            if self.player_entry[0] == 5 and self.player_entry[1] in edge_entry:
                pass   # avoid loss
            elif self.player_entry[0] == 5 and self.player_entry[1] in corner_entry:
                return random.choice(self.corner_spots)  # avoid loss else corner

            elif self.player_entry[0] in edge_entry and self.player_entry[1] in edge_entry:
                if self.smart_spot(self.player_entry):  # CCS else corner
                    print("thinking...")
                    time.sleep(1)
                    return self.smart_spot(self.player_entry)
                else:
                    return random.choice(self.corner_spots)
            elif self.player_entry[0] in edge_entry and self.player_entry[1] in corner_entry:
                print("thinking...")
                time.sleep(1)
                return self.smart_spot(self.player_entry)  # avoid loss else CCS

            elif self.player_entry[0] in corner_entry and self.player_entry[1] in edge_entry:
                return random.choice(self.corner_spots)  # avoid loss else corner
            elif self.player_entry[0] in corner_entry and self.player_entry[1] in corner_entry:
                return random.choice(self.edge_spots)  # avoid loss else edge

    def computer_move(self):
        print("Computer's Turn...")
        print("thinking...")
        time.sleep(0.5)
        if self.comp_first_turn and len(self.comp_entry) < 2:
            key = self.first_comp()
        elif not self.comp_first_turn and len(self.player_entry) < 3:
            key = self.second_comp
        else:  # after 4 move, just to look for win or avoid loose chances
            if self.win_chance(self.comp_entry):
                key = self.win_chance(self.comp_entry)
            elif self.win_chance(self.player_entry):
                key = self.win_chance(self.player_entry)
            else:
                key = random.choice(self.corner_spots + self.edge_spots)
        (r, c) = input_dict[key]
        self.update_available_spots(key)
        self.make_move(r, c)
        self.comp_entry.append(key)
        print(f"Computer entered number: {key}")


def play_again():
    wish = (input(" Want to play again(Y/N): ")).lower()
    print(wish)
    if wish and wish[0] == "n":
        print("\n  Thanks for playing")
        return False
    else:
        print("\n  Let's play again")
        return True


    

def wrong_input():
    print("""
###########################################################
##                                                       ##
##   7 8 9    WRONG ENTRY!!!                             ##
##   4 5 6 <--Enter number from 1-9 as per NumPad layout ##
##   1 2 3    to choose your spot on Tic-Tac-Toe Board   ##
##                                                       ##
###########################################################
       """)


print("""
                Welcome to TIC-TAC-TOE Game
                The spots in 3x3 tic-tac-toe board are 
                numbers on NumPad(1-9) respectively

                        _ _ _        7 8 9
                        _ _ _   ==>  4 5 6
                        _ _ _        1 2 3 

                *Who will play first will be decided randomly*

""")