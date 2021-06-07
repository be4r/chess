def check_if_move_correct(self.board, move):
    pass

def add_move_to_board(self.board, move):
    pass

def check_if_end_of_game(self.board, move):
    pass

class Board:
    def __init__(...):
        '''
            Инициализация доски. Фигуры располагаются в порядке, установленном
            правилами шахмат.
        '''
        self.pieces_positions = []
        
        # Добавление чёрных фигур
        self.pieces_positions.append(["rook1", "knight1", "bishop1", "queen1", "king1", "bishop1", "knight1", "rook1"])
        self.pieces_positions.append(["pawn1" for i in range(8)])

        # Добавление пустых полей        
        self.pieces_positions += [["empty" for i in range(8)] for i in range 4]

        # Добавление белых фигур        
        self.pieces_positions.append(["pawn0" for i in range(8)])
        self.pieces_positions.append(["rook0", "knight0", "bishop0", "queen0", "king0", "bishop0", "knight0", "rook0"])                

        self.is_check = False
        self.is_mate = False

    def get_pieces_positions(...):
        return self.pieces_positions

    def _get_all_possible_mooves(...):
        
