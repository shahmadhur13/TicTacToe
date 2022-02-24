import TicTacToe


game = TicTacToe.TicTacToe()  # creating instance of class TicTacToe

while game.check_winner() == -1:  # -1 indicate game is neither won/lose nor draw

    if game.player == 1:  # player turn
        game.print_board()
        num = (input("Enter number from NumPad(1-9):"))

        if num.isdigit() and int(num) in range(1, 10):  # check valid input

            if int(num) in game.available_entry:  # check empty spot
                (R, C) = TicTacToe.input_dict[int(num)]
                game.update_available_spots(int(num))

                game.make_move(R, C)  # only make_move function will change player turn
                game.move += 1
                game.player_entry.append(int(num))
                game.print_board()
            else:
                print("That spot is already used")
                TicTacToe.wrong_input()
                continue
        else:
            TicTacToe.wrong_input()
            continue

    if game.check_winner() == -1 and game.player == 2:  # check game is not over and comp's turn
        game.computer_move()  # (game.player_entry, game.comp_entry)
        game.move += 1

x = game.check_winner()  # evaluate game status (won/loss/draw)
if x == 0:  # no empty spots
    print("\nIt's DRAW\n")
    game.print_board()
else:
    game.print_board()
    if x == 2:  # Comp is always player 2 (symbol '0') check variable "char" index
        print("\nComputer Wins")
    else:
        print("\nYou win!")
