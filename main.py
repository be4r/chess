from backend import check_if_move_correct, add_move_to_board, check_if_end_of_game, Board

class Game:
    def __init__(...):
        self.board = Board()
        pass

    def make_move(...):
        pass

    def start(...):
        while True:
            show_board()
            move = get_move()
            if $check_if_move_correct$(self.board, move):
                $add_move_to_board$(self.board, move)
            else:
                print("You wanna do wrong thing! It's not possible.")
            if $check_if_end_of_game$(self.board, move):
                end_game()


game = Game()
Game.start()
