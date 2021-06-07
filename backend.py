def check_if_move_correct(self.board, move):
    if move in Board.get_all_possible_moves():    
        return True
    return False

def add_move_to_board(self.board, move):
    pass

def check_if_end_of_game(self.board, move):
    pass


class Board:
    def __init__(self):
        '''
            Инициализация доски. Фигуры располагаются в порядке, установленном
            правилами шахмат (от 15 века нашей эры).
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
        self.active_player = 0


    def get_pieces_positions(...):
        return self.pieces_positions

    def get_all_possible_moves(...):
        '''
            Вычисление всех возможных ходов, которые может сделать игрок. Учитывается положение фигур на доске и очерёдность хода игроков. 
        '''
        all_possible_moves = []
        for piece_raw_ind in range(len(self.pieces_positions)):
            for piece_col_ind, piece_name in enumerate(range(len(self.pieces_positions[piece_raw_ind]))):
                piece_possible_moves = self.get_piece_possible_moves(piece_name, piece_raw_ind, piece_col_ind)
                all_possible_moves += piece_possible_moves
        return all_possible_moves

        
    def get_piece_possible_moves(self, piece_name: str, piece_raw_ind: int, piece_col_ind: int):
        '''
            Вычисление всех возможных ходов заданной фигуры.
            Учитывается то, что: 
            * фигура может поставить шах
            * фигура, переместившись, может поставить своего короля под шах
            * фигуры не могут прыгать через другие фигуры (кроме коней --- они могут)
            
        '''
        if int(piece_name[-1]) != self.active_player:
            return []
        piece_possible_moves = []

        if piece_name[:-1] == "pawn":
            pass
        elif piece_name[:-1] == "rook":
            pass
        elif piece_name[:-1] == "king":
            pass
        elif piece_name[:-1] == "queen":
            pass
        elif piece_name[:-1] == "knight":
            pass
        elif piece_name[:-1] == "bishop":
            pass

        checked_piece_possible_moves = []
        for possible_move in piece_possible_moves:
            if not self.is_check_after_move(possible_move):
                checked_piece_possible_moves.append(possible_move)

        return checked_piece_possible_moves

    def is_check_after_move(move):
        

    def check_if_check(self):
        pass


    def 

        
