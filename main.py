import TicTacToe



play = True
you_won = 0
computer_won = 0
draw = 0
total_game = you_won + computer_won + draw


def score_card():
    total_game = you_won + computer_won + draw
    print(f"""
          ###############
         # ___________   #
        #  |SCORE CARD|   #
        #  ````````````   #
        # Games:    {total_game}     #
        # You:      {you_won}/{total_game}   #
        # Computer: {computer_won}/{total_game}   #
        # Draw:     {draw}/{total_game}   #
        #                 #
         #               #
          ###############
        """)

while play:
    game = TicTacToe.TicTacToe()  # creating instance of class TicTacToe
    while game.check_winner() == -1:
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
        draw += 1
        game.print_board()
        score_card()
        play = TicTacToe.play_again()
        
    else:
        game.print_board()
        if x == 2:  # Comp is always player 2 (symbol '0') check variable "char" index
            print("\nComputer Wins")
            computer_won += 1
            score_card()
            play = TicTacToe.play_again()
        else:    
            print("\nYou win!")
            you_won += 1
            score_card()
            play = TicTacToe.play_again()
            