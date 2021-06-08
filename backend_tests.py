from backend import Board, check_if_move_correct, add_move_to_board, check_if_end_of_game

def real_time_test():
    board = Board()
    while True:
        request = input("Введите следующий ход: ")
        if request == "quit" or request == "q":
            break
        elif type(eval(request)) == tuple:
            move = eval(request)
            if check_if_move_correct(board, move):
                add_move_to_board(board, move)
            else:
                print("Wrong move!")            
