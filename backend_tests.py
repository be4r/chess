from backend import Board, check_if_move_correct, add_move_to_board, check_if_end_of_game

def show_pieces(pieces_positions):
    for i in range(len(pieces_positions)):
        for j in range(len(pieces_positions[i])):
            print("{:10}".format(pieces_positions[i][j]), end=' ')
        print('\n')

def real_time_test():
    board = Board()
    show_pieces(board.get_pieces_positions())
    while True:
        board.get_all_possible_moves()
        request = input("Введите следующий ход: ")
        if request == "quit" or request == "q":
            break
        elif type(eval(request)) == tuple:
            move = eval(request)
            if check_if_move_correct(board, move):
                pawn_position = add_move_to_board(board, move)
                if pawn_position is not None:
                    user_answer = input()
                    board.change_pawn(pawn_position, user_answer.split(' ')[0])
                
                show_pieces(board.get_pieces_positions())
            else:
                print("Wrong move!")

real_time_test()            
