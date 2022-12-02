# write your code here
import random
import copy


class TicTacToe:

    def __init__(self, position_data):
        self.game_status = "playing"
        self.mode = None
        self.mode_level = "easy"
        self.table_position = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.current_player = self.check_turn()

    def __str__(self):
        return f"""---------
| {' '.join(self.table_position[0])} |
| {' '.join(self.table_position[1])} |
| {' '.join(self.table_position[2])} |
---------"""

    def check_win(self):
        if not self.check_turn():
            print("Draw")
            self.game_status = "ended"

        for i in range(3):
            if self.table_position[:][i] in [['X', 'X', 'X'], ['O', 'O', 'O']]:
                print(self.current_player + " wins")
                self.game_status = "ended"
                break
            elif [e[i] for e in self.table_position] in [['X', 'X', 'X'], ['O', 'O', 'O']]:
                print(self.current_player + " wins")
                self.game_status = "ended"
                break
            elif [self.table_position[0][0], self.table_position[1][1], self.table_position[2][2]] in [['X', 'X', 'X'],
                                                                                                       ['O', 'O', 'O']]:
                print(self.current_player + " wins")
                self.game_status = "ended"
                break
            elif [self.table_position[0][2], self.table_position[1][1], self.table_position[2][0]] in [['X', 'X', 'X'],
                                                                                                       ['O', 'O', 'O']]:
                print(self.current_player + " wins")
                self.game_status = "ended"
                break

    def check_turn(self):
        x_s = 0
        y_s = 0
        for i in self.table_position:
            for e in i:
                if e == "X":
                    x_s += 1
                elif e == "O":
                    y_s += 1
        if x_s + y_s == 9:
            return False
        elif x_s == y_s:
            return "X"
        else:
            return "O"

    def check_places(self, x, y):
        if self.table_position[x][y] == " ":
            return True
        else:
            return False

    def modify_table_user(self):
        correct_answer = False
        while not correct_answer:
            try:
                x, y = input("Enter the coordinates: >").split()

                if x.isalpha() or y.isalpha():  # Check if the inputs are characters
                    print("You should enter numbers!")

                elif int(x) not in range(1, 4) or int(y) not in range(1, 4):  # Check if the inputs are out of bound
                    print("Coordinates should be from 1 to 3!")

                else:  # Check if the inputs are in abailable places
                    x, y = int(x) - 1, int(y) - 1
                    correct_answer = self.check_places(x, y)

                    if not correct_answer:
                        print("This cell is occupied! Choose another one!")
                    else:
                        self.current_player = copy.deepcopy(self.check_turn())
                        self.table_position[x][y] = self.current_player

            except ValueError:  # Check if the inputs are two
                print("You should enter numbers!")

        print(self)
        self.check_win()
        if self.game_status == "ended":
            self.game_status = "playing"
            self.game_mode()

    # === === ===

    def easy_random_level(self):
        empty_spaces = []
        for index_x, i in enumerate(self.table_position):
            for index_y, e in enumerate(i):
                if e == " ":
                    empty_spaces.append([index_x, index_y])

        choice = random.choice(empty_spaces)
        return choice[0], choice[1]

    def modify_table_easy_mode(self):
        x, y = self.easy_random_level()
        self.current_player = copy.deepcopy(self.check_turn())
        self.table_position[x][y] = self.check_turn()

        print(f'Making move level "easy"')
        print(self)
        self.check_win()
        if self.game_status == "ended":
            self.game_status = "playing"
            self.game_mode()

    # === === ===

    def check_AI_next_move(self, x, y, character):
        draft = copy.deepcopy(self.table_position)
        draft[x][y] = character

        for i in range(3):
            if draft[:][i] in [['X', 'X', 'X'], ['O', 'O', 'O']]:
                return draft
            elif [e[i] for e in draft] in [['X', 'X', 'X'], ['O', 'O', 'O']]:
                return draft
            elif [draft[0][0], draft[1][1], draft[2][2]] in [['X', 'X', 'X'], ['O', 'O', 'O']]:
                return draft
            elif [draft[0][2], draft[1][1], draft[2][0]] in [['X', 'X', 'X'], ['O', 'O', 'O']]:
                return draft

        return False

    # === === ===

    def medium_random_level(self):
        empty_spaces = []
        possible_return_moves = []
        actual_player = self.check_turn()
        if actual_player == "O":
            actual_contender = "X"
        else:
            actual_contender = "O"

        for index_x, i in enumerate(self.table_position):
            for index_y, e in enumerate(i):
                if e == " ":
                    empty_spaces.append([index_x, index_y])

        for i in empty_spaces:
            attempt = self.check_AI_next_move(i[0], i[1], actual_player)

            if attempt:
                return i[0], i[1]

            else:
                possible_correct_move = [i[0], i[1]]
                possible_contender_move = []
                draft = copy.deepcopy(self.table_position)
                draft[i[0]][i[1]] = actual_contender

                for index_x, y in enumerate(draft):
                    for index_y, e in enumerate(y):
                        if e == " ":
                            possible_contender_move.append([index_x, index_y])

                #  print(possible_contender_move, "contender movement for", possible_correct_move)

                for w in possible_contender_move:
                    contender_movement = self.check_AI_next_move(w[0], w[1], actual_contender)
                    if contender_movement:
                        break
                else:
                    possible_return_moves.append(possible_correct_move)

        #  print(posible_return_moves) -> check all the good posible moves
        if possible_return_moves:  # if there is any good move to make, chose one of them
            if [1, 1] in possible_return_moves:
                return 1, 1
            else:
                choice = random.choice(possible_return_moves)
                return choice[0], choice[1]
        else:
            choice = random.choice(empty_spaces)  # if there's any good move, just choose a randome empty space
            return choice[0], choice[1]

    def modify_table_medium_mode(self):
        x, y = self.medium_random_level()
        self.current_player = copy.deepcopy(self.check_turn())
        self.table_position[x][y] = self.check_turn()
        print(f'Making move level "medium"')
        print(self)
        self.check_win()
        if self.game_status == "ended":
            self.game_status = "playing"
            self.game_mode()

    # === === ===

    def hard_random_level(self):
        empty_spaces = []
        possible_return_moves = []
        actual_player = self.check_turn()
        if actual_player == "O":
            actual_contender = "X"
        else:
            actual_contender = "O"

        for index_x, i in enumerate(self.table_position):
            for index_y, e in enumerate(i):
                if e == " ":
                    empty_spaces.append([index_x, index_y])

        for i in empty_spaces:
            attempt = self.check_AI_next_move(i[0], i[1], actual_player)

            if attempt:  # if it's winning in the next movement return that position.
                return i[0], i[1]
            else:
                possible_correct_move = [i[0], i[1]]
                possible_contender_move = []
                draft = copy.deepcopy(self.table_position)
                draft[i[0]][i[1]] = actual_contender

                for index_x, y in enumerate(draft):
                    for index_y, e in enumerate(y):
                        if e == " ":
                            possible_contender_move.append([index_x, index_y])

                #  print(possible_contender_move, "contender movement for", possible_correct_move)

                for w in possible_contender_move:  # check all posible movement of the contender to see if he wins.
                    contender_movement = self.check_AI_next_move(w[0], w[1], actual_contender)
                    if contender_movement:
                        break
                else:
                    possible_return_moves.append(possible_correct_move)

        #  print(possible_return_moves) -> check all the good posible moves
        if possible_return_moves:  # if there is any good move to make, chose one of them
            if [1, 1] in possible_return_moves:
                return 1, 1
            else:
                choice = random.choice(possible_return_moves)
                return choice[0], choice[1]
        else:
            choice = random.choice(empty_spaces)  # if there's any good move, just choose a randome empty space
            return choice[0], choice[1]

    def modify_table_hard_mode(self):
        x, y = self.hard_random_level()
        self.current_player = copy.deepcopy(self.check_turn())
        self.table_position[x][y] = self.check_turn()
        print(f'Making move level "hard"')
        print(self)
        self.check_win()
        if self.game_status == "ended":
            self.game_status = "playing"
            self.game_mode()

    # === === ===
    def game_mode(self):
        self.table_position = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.mode = []
        while not self.mode:
            try:
                command = input("Input command: > ")
                if command == "exit":
                    exit()
                else:
                    start_key, ply_1, ply_2 = command.split()
                    if ply_1 in ['user', 'easy', 'medium', 'hard'] and ply_2 in ['user', 'easy', 'medium', 'hard']:
                        self.mode = [start_key, ply_1, ply_2]
                    else:
                        print('Bad parameters!')
            except ValueError:
                print('Bad parameters!')
        print(self)
        self.take_turns()

    def take_turns(self):
        turn = 1
        while True:
            if self.mode[turn] == "easy":
                self.modify_table_easy_mode()
            elif self.mode[turn] == "medium":
                self.modify_table_medium_mode()
            elif self.mode[turn] == "hard":
                self.modify_table_hard_mode()
            elif self.mode[turn] == "user":
                self.modify_table_user()

            if turn == 1:
                turn = 2
            else:
                turn = 1


if __name__ == '__main__':
    print("How to start the game: start (user|easy|medium|hard) (user|easy|medium|hard) \n and press enter...")
    start = TicTacToe("_________")  # input("Enter the cells: >")
    start.game_mode()
