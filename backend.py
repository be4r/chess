import copy

def check_if_move_correct(board, move):
    '''
        Проверка корректности хода, сделанного пользователем
    '''
    all_possible_moves = board.get_all_possible_moves()
    print(all_possible_moves)
    if move in all_possible_moves:    
        return True
    return False

def add_move_to_board(board, move):
    '''
        Добавление одного хода на доску. Предполагается, что этот ход корректен. В данной функции нет проверки корректности хода.
        Функция также проверяет, дошла ли какая-либо пешка на данном ходе до "дамок". Если дошла, то функция возвращает
        координаты этой пешки. Если ни одна пешка до "дамок" не дошла, то возвращается None
    '''
    board.pieces_positions[move[1][0]][move[1][1]] = board.pieces_positions[move[0][0]][move[0][1]]
    board.pieces_positions[move[0][0]][move[0][1]] = "empty"
    last_pawn_position = board.check_pawns()
    board.active_player = 1 - board.active_player
    return last_pawn_position

def check_if_end_of_game(board, move):
    '''
        Проверка того, случился ли мат или пат.
    '''
    if not board.get_all_possible_moves():
        print("HAHAHAHAHHAAHAH")
        if board.check_if_check():
            # Мат            
            return True, 'checkmate'
        else:
            # Пат
            return True, 'stalemate'
    return False, None


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
        self.pieces_positions += [["empty" for i in range(8)] for j in range(4)]

        # Добавление белых фигур        
        self.pieces_positions.append(["pawn0" for i in range(8)])
        self.pieces_positions.append(["rook0", "knight0", "bishop0", "queen0", "king0", "bishop0", "knight0", "rook0"])                

        self.is_check = False
        self.is_mate = False
        self.active_player = 0

        self.previous_move = None

    def check_pawns(self):
        last_raw_ind =  7 * self.active_player
        for col_ind in range(8):
            if self.pieces_positions[last_raw_ind][col_ind] == "pawn{}".format(self.active_player):
                print("|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n")
                return True

        return False
    
    def change_piece(self, position, new_piece_name):
        '''
            Замена фигуры на другую фигуру того же цвета.
        '''
        prev_piece_name = self.pieces_positions[position[0]][position[1]]
        if prev_piece_name == "empty":
            print("На данной позиции нет фигуры!")
            return
        if new_piece_name[-1] == '0' or new_piece_name[-1] == '1':
            self.pieces_positions[position[0]][position[1]] = new_piece_name
        else:
            self.pieces_positions[position[0]][position[1]] = new_piece_name + prev_piece_name[-1]

    def change_pawn(self, position, new_piece_name):
        if new_piece_name == "queen" or new_piece_name == "rook" or new_piece_name == "bishop" or\
            new_piece_name == "knight":
            self.change_piece(self, position, new_piece_name)
        else:
            print("Вы пытаетесь заменить пешку на какую-то странную фигуру ({}).".format(new_piece_name))
            print("Её можно заменить только на королеву (queen), ладью (rook), слона (bishop) и коня (knight).")         



    def get_pieces_positions(self):
        return self.pieces_positions

    def get_all_possible_moves(self, check_for_check=True):
        '''
            Вычисление всех возможных ходов, которые может сделать игрок. Учитывается положение фигур на доске и очерёдность хода игроков. 
        '''
        all_possible_moves = []
        for piece_raw_ind in range(len(self.pieces_positions)):
            for piece_col_ind, piece_name in enumerate(self.pieces_positions[piece_raw_ind]):
                piece_possible_moves = self.get_piece_possible_moves(piece_name, piece_raw_ind, piece_col_ind, check_for_check=check_for_check)
                all_possible_moves += piece_possible_moves
        return all_possible_moves

        
    def get_piece_possible_moves(self, piece_name: str, piece_raw_ind: int, piece_col_ind: int, check_for_check=True):
        '''
            Вычисление всех возможных ходов заданной фигуры.
            Учитывается то, что: 
            * фигура может поставить шах
            * фигура, переместившись, может поставить своего короля под шах
            * фигуры не могут прыгать через другие фигуры (кроме коней --- они могут)
            
        '''
        #print(piece_name)
        if piece_name == "empty":
            return []
        if int(piece_name[-1]) != self.active_player:
            return []
        piece_possible_moves = []

        if piece_name[:-1] == "pawn":
            piece_possible_moves = self.get_pawn_possible_moves(piece_raw_ind, piece_col_ind)
        elif piece_name[:-1] == "rook":          
            piece_possible_moves = self.get_rook_possible_moves(piece_raw_ind, piece_col_ind)
        elif piece_name[:-1] == "king":
            piece_possible_moves = self.get_king_possible_moves(piece_raw_ind, piece_col_ind)
        elif piece_name[:-1] == "queen":
            piece_possible_moves = self.get_queen_possible_moves(piece_raw_ind, piece_col_ind)
        elif piece_name[:-1] == "knight":
            piece_possible_moves = self.get_knight_possible_moves(piece_raw_ind, piece_col_ind)
        elif piece_name[:-1] == "bishop":
            piece_possible_moves = self.get_bishop_possible_moves(piece_raw_ind, piece_col_ind)
       
        if not check_for_check:
            return piece_possible_moves
            
        checked_piece_possible_moves = []
        for possible_move in piece_possible_moves:
            if not self.is_check_after_move(possible_move):
                checked_piece_possible_moves.append(possible_move)
        
        #print(piece_name)
        #for move in checked_piece_possible_moves:
        #    print(move)
        return checked_piece_possible_moves

    def get_pawn_possible_moves(self, piece_raw_ind: int, piece_col_ind: int):
        pawn_possible_moves = []        
        pawn_step = self.active_player * 2 - 1

        # Ход вперёд
        if self.pieces_positions[piece_raw_ind + pawn_step][piece_col_ind] == "empty":
            pawn_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind + pawn_step, piece_col_ind)))

        # Поедание фигур справа-спереди и слева-спереди
        if piece_col_ind != 7:
            right_forward_piece_name = self.pieces_positions[piece_raw_ind + pawn_step][piece_col_ind + 1]        
            if right_forward_piece_name != "empty" and int(right_forward_piece_name[-1]) == 1 - self.active_player:
                pawn_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind + pawn_step, piece_col_ind + 1)))
      
        if piece_col_ind != 0:
            left_forward_piece_name = self.pieces_positions[piece_raw_ind + pawn_step][piece_col_ind - 1]
            if left_forward_piece_name != "empty" and int(left_forward_piece_name[-1]) == 1 - self.active_player:
                pawn_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind + pawn_step, piece_col_ind - 1)))
                               
        # Первый ход пешки на 2 поля вперёд
        if piece_raw_ind - pawn_step == 7 * (1 - self.active_player):
            pawn_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind + 2 * pawn_step, piece_col_ind)))
            
        return pawn_possible_moves            


    def get_rook_possible_moves(self, piece_raw_ind: int, piece_col_ind: int):
        rook_possible_moves = []
        
        # Проверить все поля, находящиеся ниже ладьи
        for current_raw_ind in range(piece_raw_ind + 1, 8):
            if self.pieces_positions[current_raw_ind][piece_col_ind] == "empty":
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind),(current_raw_ind, piece_col_ind)))
            elif int(self.pieces_positions[current_raw_ind][piece_col_ind][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[current_raw_ind][piece_col_ind][-1]) == 1 - self.active_player:
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind),(current_raw_ind, piece_col_ind)))
                break            

        # Проверить все поля, находящиеся выше ладьи
        for current_raw_ind in range(piece_raw_ind - 1, -1, -1):
            if self.pieces_positions[current_raw_ind][piece_col_ind] == "empty":
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind),(current_raw_ind, piece_col_ind)))
            elif int(self.pieces_positions[current_raw_ind][piece_col_ind][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[current_raw_ind][piece_col_ind][-1]) == 1 - self.active_player:
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind),(current_raw_ind, piece_col_ind)))
                break            

        # Проверить все поля, находящиеся правее ладьи
        for current_col_ind in range(piece_col_ind + 1, 8):
            if self.pieces_positions[piece_raw_ind][current_col_ind] == "empty":
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind),(piece_raw_ind, current_col_ind)))
            elif int(self.pieces_positions[piece_raw_ind][current_col_ind][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[piece_raw_ind][current_col_ind][-1]) == 1 - self.active_player:
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind),(piece_raw_ind, current_col_ind)))
                break            

        # Проверить все поля, находящиеся правее ладьи
        for current_col_ind in range(piece_col_ind - 1, -1, -1):
            if self.pieces_positions[piece_raw_ind][current_col_ind] == "empty":
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind),(piece_raw_ind, current_col_ind)))
            elif int(self.pieces_positions[piece_raw_ind][current_col_ind][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[piece_raw_ind][current_col_ind][-1]) == 1 - self.active_player:
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind),(piece_raw_ind, current_col_ind)))
                break    

        return rook_possible_moves

    def get_bishop_possible_moves(self, piece_raw_ind: int, piece_col_ind: int):
        bishop_possible_moves = []
        
        # Проверить все поля, находящиеся выше-слева слона
        for offset in range(-1, -1 * min(piece_raw_ind, piece_col_ind) - 1, -1):
            if self.pieces_positions[piece_raw_ind + offset][piece_col_ind + offset] == "empty":
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind),(piece_raw_ind + offset, piece_col_ind + offset)))
            elif int(self.pieces_positions[piece_raw_ind + offset][piece_col_ind + offset][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[piece_raw_ind + offset][piece_col_ind + offset][-1]) == 1 - self.active_player:
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind),(piece_raw_ind + offset, piece_col_ind + offset)))
                break            

        # Проверить все поля, находящиеся ниже-справа слона
        for offset in range(-1, -1 * min(7 - piece_raw_ind, 7 - piece_col_ind) - 1, -1):
            if self.pieces_positions[piece_raw_ind - offset][piece_col_ind - offset] == "empty":
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind),(piece_raw_ind - offset, piece_col_ind - offset)))
            elif int(self.pieces_positions[piece_raw_ind - offset][piece_col_ind - offset][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[piece_raw_ind - offset][piece_col_ind - offset][-1]) == 1 - self.active_player:
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind),(piece_raw_ind - offset, piece_col_ind - offset)))
                break            

        # Проверить все поля, находящиеся ниже-слева слона
        for offset in range(-1, -1 * min(7 - piece_raw_ind, piece_col_ind) - 1, -1):
            if self.pieces_positions[piece_raw_ind - offset][piece_col_ind + offset] == "empty":
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind),(piece_raw_ind - offset, piece_col_ind + offset)))
            elif int(self.pieces_positions[piece_raw_ind - offset][piece_col_ind + offset][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[piece_raw_ind - offset][piece_col_ind + offset][-1]) == 1 - self.active_player:
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind),(piece_raw_ind - offset, piece_col_ind + offset)))
                break            

        # Проверить все поля, находящиеся выше-справа слона
        for offset in range(-1, -1 * min(piece_raw_ind, 7 - piece_col_ind) - 1, -1):
            if self.pieces_positions[piece_raw_ind + offset][piece_col_ind - offset] == "empty":
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind),(piece_raw_ind + offset, piece_col_ind - offset)))
            elif int(self.pieces_positions[piece_raw_ind + offset][piece_col_ind - offset][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[piece_raw_ind + offset][piece_col_ind - offset][-1]) == 1 - self.active_player:
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind),(piece_raw_ind + offset, piece_col_ind - offset)))
                break            

        return bishop_possible_moves

    def get_queen_possible_moves(self, piece_raw_ind: int, piece_col_ind: int):
        queen_possible_moves = []
        queen_possible_moves += self.get_rook_possible_moves(piece_raw_ind, piece_col_ind)
        queen_possible_moves += self.get_bishop_possible_moves(piece_raw_ind, piece_col_ind)
        return queen_possible_moves

    def get_king_possible_moves(self, piece_raw_ind: int, piece_col_ind: int):
        offsets = [
                   (-1, -1), (-1, 0), (-1, 1),
                   ( 0, -1),          ( 0, 1),
                   ( 1, -1), ( 1, 0), ( 1, 1) 
                  ]
        
        king_possible_moves = []
        for raw_offset, col_offset in offsets:
            new_raw_ind = piece_raw_ind + raw_offset
            new_col_ind = piece_col_ind + col_offset
            if 0 <= new_raw_ind <= 7 and 0 <= new_col_ind <= 7:
                if self.pieces_positions[new_raw_ind][new_col_ind] == "empty" or\
                    int(self.pieces_positions[new_raw_ind][new_col_ind][-1]) == 1 - self.active_player:
                    king_possible_moves.append(((piece_raw_ind, piece_col_ind), (new_raw_ind, new_col_ind)))
        return king_possible_moves    
            
    

    def get_knight_possible_moves(self, piece_raw_ind: int, piece_col_ind: int):
        offsets = [
                   (-1, -2), (-2, -1),
                   (-1,  2), (-2,  1),
                   ( 1,  2), ( 2,  1),
                   ( 1, -2), ( 2, -1)
                  ]
        
        knight_possible_moves = []
        for raw_offset, col_offset in offsets:
            new_raw_ind = piece_raw_ind + raw_offset
            new_col_ind = piece_col_ind + col_offset
            if 0 <= new_raw_ind <= 7 and 0 <= new_col_ind <= 7:
                if self.pieces_positions[new_raw_ind][new_col_ind] == "empty" or\
                    int(self.pieces_positions[new_raw_ind][new_col_ind][-1]) == 1 - self.active_player:
                    knight_possible_moves.append(((piece_raw_ind, piece_col_ind), (new_raw_ind, new_col_ind)))
        return knight_possible_moves    


    
    def is_check_after_move(self, move: tuple):
        virtual_board = copy.deepcopy(self)
        # saved_pieces_positions = self.pieces_positions
        add_move_to_board(virtual_board, move)
        is_check = virtual_board.check_if_check()
        #self.pieces_positions = saved_pieces_positions
        return is_check

    def check_if_check(self):
        saved_active_player = self.active_player
        #self.active_player = 1 - self.active_player
        print(self.active_player)
        possible_moves = self.get_all_possible_moves(check_for_check=False)
        #self.active_player = saved_active_player
        print(1 - saved_active_player)
        king_position = self.find_king_position(1 - saved_active_player)
        print(king_position)
        for move in possible_moves:
            if move[1] == king_position:
                return True
        return False


    def find_king_position(self, player_id: int):
        king_full_name = "king{}".format(player_id)
        for raw_ind in range(len(self.pieces_positions)):
            for col_ind, piece_name in enumerate(self.pieces_positions[raw_ind]):
                if piece_name == king_full_name:
                    return (raw_ind, col_ind) 






        
