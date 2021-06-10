"""
Бэкенд проекта.

Этот модуль содержит функции и класс, реализующие бэкэнд-составляющую проекта.
Здесь вы можете найти реализацию класса Board, соответствующего виртуальной шахматной доске.
Другие имеющиеся функции нужны для взаимодействия с классом Board.

"""

import copy


def check_if_move_correct(board, move):
    """
    Проверка корректности хода.

    :param board: Виртуальная шахматная доска в некотором состоянии игры. Объект класса Board
    :param move: Проверяемый на корректность ход. Объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))

    :return: True, если ход корректный, False --- иначе
    """
    all_possible_moves = board.get_all_possible_moves()
    if board.debug:
        print(all_possible_moves)
    if move in all_possible_moves:
        return True
    return False


def add_move_to_board(board, move):
    """
    Добавление одного хода на доску. Предполагается, что этот ход корректен.

    В данной функции нет проверки корректности хода.
    Функция также проверяет, дошла ли какая-либо пешка на данном ходе до "дамок".
    Если дошла, то функция возвращает
    координаты этой пешки. Если ни одна пешка до "дамок" не дошла, то возвращается None.

    :param board: Виртуальная шахматная доска в некотором состоянии игры. Объект класса Board
    :param move: Совершаемый ход. Объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))

    :return: True, если на совершённом ходу пешка дошла до "дамок", False --- иначе
    """
    # Поддержание состояний короля и ладий. Потребуется для проверки корректности рокировки
    if board.pieces_positions[move[0][0]][move[0][1]][:-1] == "king":
        board.king_moved[board.active_player] = True
    if board.pieces_positions[move[0][0]][move[0][1]][:-1] == "rook":
        if move[0][1] == 0 and move[0][0] == 7 * (1 - board.active_player):
            board.left_rook_moved[board.active_player] = True
        elif move[0][1] == 7 and move[0][0] == 7 * (1 - board.active_player):
            board.right_rook_moved[board.active_player] = True

    # Совершение стандартного хода
    board.pieces_positions[move[1][0]][move[1][1]] = board.pieces_positions[move[0][0]][move[0][1]]
    board.pieces_positions[move[0][0]][move[0][1]] = "empty"

    # Дополнительные действия для обработки взятия пешки пешкой "на проходе"
    if check_pawn_extramove(board, move):
        board.pieces_positions[move[0][0]][move[1][1]] = "empty"

    # Дополнительные действия для обработки рокировки
    if check_king_castling(board, move):
        print("CASTLING")
        if move[0][1] < move[1][1]:
            # Случай короткой рокировки
            add_move_to_board(board, ((7 * (1 - board.active_player), 7), (7 * (1 - board.active_player), 5)))
        elif move[0][1] > move[1][1]:
            # Случай длинной рокировки
            add_move_to_board(board, ((7 * (1 - board.active_player), 0), (7 * (1 - board.active_player), 3)))
        board.active_player = 1 - board.active_player

    # Дополнительные действия для проверкки того, дошла ли какая-то пешка до "дамок"
    last_pawn_position = board.check_pawns()
    board.active_player = 1 - board.active_player
    board.previous_move = move
    return last_pawn_position


def check_king_castling(board, move):
    """
    Проверка того, является ли ход рокировкой.

    :param board: Виртуальная шахматная доска в некотором состоянии игры. Объект класса Board
    :param move: Проверяемый ход. Объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))

    :return: True, если ход является рокировкой, False --- иначе
    """
    if board.pieces_positions[move[1][0]][move[1][1]][:-1] == "king" and \
            abs(move[0][1] - move[1][1]) == 2:
        return True
    return False


def check_pawn_extramove(board, move):
    """
    Проверка того, является ли ход взятием пешки пешкой на проходе.

    :param board: Виртуальная шахматная доска в некотором состоянии игры. Объект класса Board
    :param move: Проверяемый ход. Объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))

    :return: True, если ход является взятием пешки на проходе, False --- иначе
    """
    if board.pieces_positions[move[0][0]][move[1][1]] == "pawn{}".format(1 - board.active_player) and \
            board.previous_move[0] == (move[0][0] + 2 * (2 * board.active_player - 1), move[1][1]) and \
            board.previous_move[1] == (move[0][0], move[1][1]):
        return True
    return False


def check_if_end_of_game(board, move):
    """
    Проверка того, завершилась ли игра матом или патом.

    :param board: Виртуальная шахматная доска в некотором состоянии игры. Объект класса Board
    :param move: Проверяемый ход. Объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))

    :return: True, checkmate{i} --- если игра завершилась матом и выиграл i-й игрок.
             True, stalemate --- если игра завершилась патом.
             False, None --- если игра не завершилась.
    """
    if not board.get_all_possible_moves():
        if board.check_if_check():
            # Мат
            return True, 'checkmate{}'.format(board.active_player)
        else:
            # Пат
            return True, 'stalemate'
    return False, None


class Board:
    """Класс, реализующий виртуальную шахматную доску."""

    def __init__(self, debug=False):
        """
        Инициализация доски.

        Фигуры располагаются в порядке, установленном правилами шахмат (от 15 века нашей эры).

        :param debug: Флаг вывода дебаг-текста. По дефолту дебаг-вывод отключен.

        :return: None
        """
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
        self.debug = debug

        self.king_moved = [False, False]
        self.right_rook_moved = [False, False]
        self.left_rook_moved = [False, False]

    def check_pawns(self):
        """
        Проверка того, дошла ли хотя бы одна пешка до "дамок" на текущем ходу.

        :return: None
        """
        last_raw_ind = 7 * self.active_player
        for col_ind in range(8):
            if self.pieces_positions[last_raw_ind][col_ind] == "pawn{}".format(self.active_player):
                if self.debug:
                    print("|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n")
                return (last_raw_ind, col_ind)

        return None

    def change_piece(self, position, new_piece_name):
        """
        Замена фигуры на другую фигуру того же цвета.

        :param position: Координаты на виртуальной доске фигуры, которую нужно заменить
        :param new_piece_name: Название фигуры, на которую нужно заменить текущую фигуру.

        :return: None
        """
        prev_piece_name = self.pieces_positions[position[0]][position[1]]
        if prev_piece_name == "empty":
            print("На данной позиции нет фигуры!")
            return
        if new_piece_name[-1] == '0' or new_piece_name[-1] == '1':
            self.pieces_positions[position[0]][position[1]] = new_piece_name
        else:
            self.pieces_positions[position[0]][position[1]] = new_piece_name + prev_piece_name[-1]

    def change_pawn(self, position, new_piece_name):
        """
        Замена пешки на слона, коня, ладью или королеву того же цвета.

        :param position: Координаты на виртуальной доске пешки, которую нужно заменить
        :param new_piece_name: Название фигуры, на которую нужно заменить пешку.

        :return: None
        """
        if new_piece_name == "queen" or new_piece_name == "rook" or new_piece_name == "bishop" or \
                new_piece_name == "knight":
            self.change_piece(position, new_piece_name)
        else:
            print("Вы пытаетесь заменить пешку на какую-то странную фигуру ({}).".format(new_piece_name))
            print("Её можно заменить только на королеву (queen), ладью (rook), слона (bishop) и коня (knight).")

    def get_pieces_positions(self):
        """
        Получение координат позиций всех фигур на виртуальной шахматной доске.

        :return: Список списков, имитирующий двумерный массив. Каждая клетка содержит название фигуры и
                 принадлежность этой фигуры к одному из игроков. Если фигуры на данной клетке нет, то там написано "empty".
        """
        return self.pieces_positions

    def get_all_possible_moves(self, check_for_check=True):
        """
        Вычисление всех возможных ходов, которые может сделать игрок.

        Учитывается положение фигур на доске и очерёдность хода игроков.

        :param check_for_check: Проверять ли, есть ли шах на доске в данный момент.

        :return: Список всевозможных ходов при текущем состоянии доски.
                 Ход --- объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))
        """
        all_possible_moves = []
        for piece_raw_ind in range(len(self.pieces_positions)):
            for piece_col_ind, piece_name in enumerate(self.pieces_positions[piece_raw_ind]):
                piece_possible_moves = self.get_piece_possible_moves(piece_name, piece_raw_ind, piece_col_ind, check_for_check=check_for_check)
                all_possible_moves += piece_possible_moves
        return all_possible_moves

    def get_piece_possible_moves(self, piece_name:
                                 str, piece_raw_ind:
                                 int, piece_col_ind:
                                 int, check_for_check=True):
        """
        Вычисление всех возможных ходов заданной фигуры.

        Учитывается то, что:
        * фигура может поставить шах
        * фигура, переместившись, может поставить своего короля под шах
        * фигуры не могут прыгать через другие фигуры (кроме коней --- они могут)

        :param piece_name: Название фигуры.
        :param piece_raw_ind: Координата строки, в которой располагается фигура.
        :param piece_col_ind: Координата столбца, в котором располагается фигура.
        :param check_for_check: Проверять ли, есть ли шах на доске в данный момент.

        :return: Список всевозможных ходов при текущем состоянии доски.
                 Ход --- объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))
        """
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

        return checked_piece_possible_moves

    def get_pawn_possible_moves(self, piece_raw_ind:
                                int, piece_col_ind:
                                int):
        """
        Вычисление всех возможных ходов пешки.

        :param piece_raw_ind: Координата строки, в которой располагается пешка.
        :param piece_col_ind: Координата столбца, в котором располагается пешка.

        :return: Список всевозможных ходов текущей пешки при текущем состоянии доски.
                 Ход --- объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))
        """
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
        if piece_raw_ind - pawn_step == 7 * (1 - self.active_player) and \
                self.pieces_positions[piece_raw_ind + pawn_step][piece_col_ind] == "empty" and \
                self.pieces_positions[piece_raw_ind + 2 * pawn_step][piece_col_ind] == "empty":
            pawn_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind + 2 * pawn_step, piece_col_ind)))

        # Правило съедания пешки "на проходе"
        if piece_raw_ind == 7 * self.active_player - 3 * pawn_step and \
                self.pieces_positions[self.previous_move[1][0]][self.previous_move[1][1]] == "pawn{}".format(1 - self.active_player) and \
                abs(self.previous_move[1][0] - self.previous_move[0][0]) == 2 and abs(self.previous_move[1][1] - piece_col_ind) == 1:
            pawn_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind + pawn_step, self.previous_move[1][1])))

        return pawn_possible_moves

    def get_rook_possible_moves(self, piece_raw_ind:
                                int, piece_col_ind:
                                int):
        """
        Вычисление всех возможных ходов ладьи.

        :param piece_raw_ind: Координата строки, в которой располагается ладья.
        :param piece_col_ind: Координата столбца, в котором располагается ладья.

        :return: Список всевозможных ходов текущей ладьи при текущем состоянии доски.
                 Ход --- объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))
        """
        rook_possible_moves = []

        # Проверить все поля, находящиеся ниже ладьи
        for current_raw_ind in range(piece_raw_ind + 1, 8):
            if self.pieces_positions[current_raw_ind][piece_col_ind] == "empty":
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind), (current_raw_ind, piece_col_ind)))
            elif int(self.pieces_positions[current_raw_ind][piece_col_ind][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[current_raw_ind][piece_col_ind][-1]) == 1 - self.active_player:
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind), (current_raw_ind, piece_col_ind)))
                break

        # Проверить все поля, находящиеся выше ладьи
        for current_raw_ind in range(piece_raw_ind - 1, -1, -1):
            if self.pieces_positions[current_raw_ind][piece_col_ind] == "empty":
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind), (current_raw_ind, piece_col_ind)))
            elif int(self.pieces_positions[current_raw_ind][piece_col_ind][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[current_raw_ind][piece_col_ind][-1]) == 1 - self.active_player:
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind), (current_raw_ind, piece_col_ind)))
                break

        # Проверить все поля, находящиеся правее ладьи
        for current_col_ind in range(piece_col_ind + 1, 8):
            if self.pieces_positions[piece_raw_ind][current_col_ind] == "empty":
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind, current_col_ind)))
            elif int(self.pieces_positions[piece_raw_ind][current_col_ind][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[piece_raw_ind][current_col_ind][-1]) == 1 - self.active_player:
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind, current_col_ind)))
                break

        # Проверить все поля, находящиеся правее ладьи
        for current_col_ind in range(piece_col_ind - 1, -1, -1):
            if self.pieces_positions[piece_raw_ind][current_col_ind] == "empty":
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind, current_col_ind)))
            elif int(self.pieces_positions[piece_raw_ind][current_col_ind][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[piece_raw_ind][current_col_ind][-1]) == 1 - self.active_player:
                rook_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind, current_col_ind)))
                break

        return rook_possible_moves

    def get_bishop_possible_moves(self, piece_raw_ind:
                                  int, piece_col_ind:
                                  int):
        """
        Вычисление всех возможных ходов слона.

        :param piece_raw_ind: Координата строки, в которой располагается слон.
        :param piece_col_ind: Координата столбца, в котором располагается слон.

        :return: Список всевозможных ходов текущего слона при текущем состоянии доски.
                 Ход --- объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))
        """
        bishop_possible_moves = []

        # Проверить все поля, находящиеся выше-слева слона
        for offset in range(-1, -1 * min(piece_raw_ind, piece_col_ind) - 1, -1):
            if self.pieces_positions[piece_raw_ind + offset][piece_col_ind + offset] == "empty":
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind + offset, piece_col_ind + offset)))
            elif int(self.pieces_positions[piece_raw_ind + offset][piece_col_ind + offset][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[piece_raw_ind + offset][piece_col_ind + offset][-1]) == 1 - self.active_player:
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind + offset, piece_col_ind + offset)))
                break

        # Проверить все поля, находящиеся ниже-справа слона
        for offset in range(-1, -1 * min(7 - piece_raw_ind, 7 - piece_col_ind) - 1, -1):
            if self.pieces_positions[piece_raw_ind - offset][piece_col_ind - offset] == "empty":
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind - offset, piece_col_ind - offset)))
            elif int(self.pieces_positions[piece_raw_ind - offset][piece_col_ind - offset][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[piece_raw_ind - offset][piece_col_ind - offset][-1]) == 1 - self.active_player:
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind - offset, piece_col_ind - offset)))
                break

        # Проверить все поля, находящиеся ниже-слева слона
        for offset in range(-1, -1 * min(7 - piece_raw_ind, piece_col_ind) - 1, -1):
            if self.pieces_positions[piece_raw_ind - offset][piece_col_ind + offset] == "empty":
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind - offset, piece_col_ind + offset)))
            elif int(self.pieces_positions[piece_raw_ind - offset][piece_col_ind + offset][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[piece_raw_ind - offset][piece_col_ind + offset][-1]) == 1 - self.active_player:
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind - offset, piece_col_ind + offset)))
                break

        # Проверить все поля, находящиеся выше-справа слона
        for offset in range(-1, -1 * min(piece_raw_ind, 7 - piece_col_ind) - 1, -1):
            if self.pieces_positions[piece_raw_ind + offset][piece_col_ind - offset] == "empty":
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind + offset, piece_col_ind - offset)))
            elif int(self.pieces_positions[piece_raw_ind + offset][piece_col_ind - offset][-1]) == self.active_player:
                break
            elif int(self.pieces_positions[piece_raw_ind + offset][piece_col_ind - offset][-1]) == 1 - self.active_player:
                bishop_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind + offset, piece_col_ind - offset)))
                break

        return bishop_possible_moves

    def get_queen_possible_moves(self, piece_raw_ind:
                                 int, piece_col_ind:
                                 int):
        """
        Вычисление всех возможных ходов королевы.

        :param piece_raw_ind: Координата строки, в которой располагается королева.
        :param piece_col_ind: Координата столбца, в котором располагается королева.

        :return: Список всевозможных ходов текущей королевы при текущем состоянии доски.
                 Ход --- объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))
        """
        queen_possible_moves = []
        queen_possible_moves += self.get_rook_possible_moves(piece_raw_ind, piece_col_ind)
        queen_possible_moves += self.get_bishop_possible_moves(piece_raw_ind, piece_col_ind)
        return queen_possible_moves

    def get_king_possible_moves(self, piece_raw_ind:
                                int, piece_col_ind:
                                int):
        """
        Вычисление всех возможных ходов короля.

        :param piece_raw_ind: Координата строки, в которой располагается король.
        :param piece_col_ind: Координата столбца, в котором располагается король.

        :return: Список всевозможных ходов короля при текущем состоянии доски.
                 Ход --- объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))
        """
        offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        king_possible_moves = []
        for raw_offset, col_offset in offsets:
            new_raw_ind = piece_raw_ind + raw_offset
            new_col_ind = piece_col_ind + col_offset
            if 0 <= new_raw_ind <= 7 and 0 <= new_col_ind <= 7:
                if self.pieces_positions[new_raw_ind][new_col_ind] == "empty" or \
                        int(self.pieces_positions[new_raw_ind][new_col_ind][-1]) == 1 - self.active_player:
                    king_possible_moves.append(((piece_raw_ind, piece_col_ind), (new_raw_ind, new_col_ind)))

        # Короткая рокировка
        if not self.king_moved[self.active_player] and not self.right_rook_moved[self.active_player] and \
                self.pieces_positions[piece_raw_ind][piece_col_ind + 1] == "empty" and \
                self.pieces_positions[piece_raw_ind][piece_col_ind + 2] == "empty" and \
                not self.check_if_check() and \
                not self.is_check_after_move(((piece_raw_ind, piece_col_ind), (piece_raw_ind, piece_col_ind + 1))):

            king_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind, piece_col_ind + 2)))

        # Длинная рокировка
        if not self.king_moved[self.active_player] and not self.left_rook_moved[self.active_player] and \
                self.pieces_positions[piece_raw_ind][piece_col_ind - 1] == "empty" and \
                self.pieces_positions[piece_raw_ind][piece_col_ind - 2] == "empty" and \
                self.pieces_positions[piece_raw_ind][piece_col_ind - 3] == "empty" and \
                not self.check_if_check() and \
                not self.is_check_after_move(((piece_raw_ind, piece_col_ind), (piece_raw_ind, piece_col_ind - 1))):

            king_possible_moves.append(((piece_raw_ind, piece_col_ind), (piece_raw_ind, piece_col_ind - 2)))

        return king_possible_moves

    def get_knight_possible_moves(self, piece_raw_ind:
                                  int, piece_col_ind:
                                  int):
        """
        Вычисление всех возможных ходов коня.

        :param piece_raw_ind: Координата строки, в которой располагается конь.
        :param piece_col_ind: Координата столбца, в котором располагается конь.

        :return: Список всевозможных ходов текущего коня при текущем состоянии доски.
                 Ход --- объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))
        """
        offsets = [
            (-1, -2), (-2, -1),
            (-1, 2), (-2, 1),
            (1, 2), (2, 1),
            (1, -2), (2, -1)
        ]

        knight_possible_moves = []
        for raw_offset, col_offset in offsets:
            new_raw_ind = piece_raw_ind + raw_offset
            new_col_ind = piece_col_ind + col_offset
            if 0 <= new_raw_ind <= 7 and 0 <= new_col_ind <= 7:
                if self.pieces_positions[new_raw_ind][new_col_ind] == "empty" or \
                        int(self.pieces_positions[new_raw_ind][new_col_ind][-1]) == 1 - self.active_player:
                    knight_possible_moves.append(((piece_raw_ind, piece_col_ind), (new_raw_ind, new_col_ind)))
        return knight_possible_moves

    def is_check_after_move(self, move: tuple):
        """
        Проверка того, будет ли на доске шах после совершения заданного хода.

        :param move: Ход --- объект класса tuple, формат следующий ((prev_raw, prev_col), (new_raw, new_col))

        :return: True, если после заданного хода на доске будет шах, False --- иначе
        """
        virtual_board = copy.deepcopy(self)
        add_move_to_board(virtual_board, move)
        virtual_board.active_player = 1 - virtual_board.active_player
        is_check = virtual_board.check_if_check()
        return is_check

    def find_king_position(self, player_id: int):
        """
        Поиск координат позиции короля на доске.

        :param player_id: 0, если ищется белый король, 1, если чёрный.

        :return: Координаты найденного короля. Объект класса tuple.
        """
        king_full_name = "king{}".format(player_id)
        for raw_ind in range(len(self.pieces_positions)):
            for col_ind, piece_name in enumerate(self.pieces_positions[raw_ind]):
                if piece_name == king_full_name:
                    return (raw_ind, col_ind)

    def check_if_check(self):
        """
        Проверка наличия шаха на доске.

        :return: True, если на доске есть шах, False --- иначе.
        """
        king_position = self.find_king_position(self.active_player)

        # Проверить, угрожают ли королю пешки
        pawn_step = 2 * self.active_player - 1
        if king_position[0] != 7 * self.active_player:
            # Пешка слева
            if king_position[1] != 0:
                if self.pieces_positions[king_position[0] + pawn_step][king_position[1] - 1] == "pawn{}".format(1 - self.active_player):
                    return True
            # Пешка справа
            if king_position[1] != 7:
                if self.pieces_positions[king_position[0] + pawn_step][king_position[1] + 1] == "pawn{}".format(1 - self.active_player):
                    return True

        # Проверить, угрожают ли королю кони
        knight_offsets = [
            (-1, -2), (-2, -1),
            (-1, 2), (-2, 1),
            (1, 2), (2, 1),
            (1, -2), (2, -1)
        ]

        for raw_offset, col_offset in knight_offsets:
            new_raw_ind = king_position[0] + raw_offset
            new_col_ind = king_position[1] + col_offset
            if 0 <= new_raw_ind <= 7 and 0 <= new_col_ind <= 7:
                if self.pieces_positions[new_raw_ind][new_col_ind] == "knight{}".format(1 - self.active_player):
                    return True

        # Првоерить, угрожают ли королю ладьи (и королевы по вертикальному и боковому направлениям)

        # Проверить все поля, находящиеся ниже короля
        for current_raw_ind in range(king_position[0] + 1, 8):
            if self.pieces_positions[current_raw_ind][king_position[1]] == "rook{}".format(1 - self.active_player) or \
                    self.pieces_positions[current_raw_ind][king_position[1]] == "queen{}".format(1 - self.active_player):
                return True
            elif self.pieces_positions[current_raw_ind][king_position[1]] == "empty":
                pass
            else:
                break
        # Проверить все поля, находящиеся выше короля
        for current_raw_ind in range(king_position[0] - 1, -1, -1):
            if self.pieces_positions[current_raw_ind][king_position[1]] == "rook{}".format(1 - self.active_player) or \
                    self.pieces_positions[current_raw_ind][king_position[1]] == "queen{}".format(1 - self.active_player):
                return True
            elif self.pieces_positions[current_raw_ind][king_position[1]] == "empty":
                pass
            else:
                break

        # Проверить все поля, находящиеся правее короля
        for current_col_ind in range(king_position[1] + 1, 8):
            if self.pieces_positions[king_position[0]][current_col_ind] == "rook{}".format(1 - self.active_player) or \
                    self.pieces_positions[king_position[0]][current_col_ind] == "queen{}".format(1 - self.active_player):
                return True
            elif self.pieces_positions[king_position[0]][current_col_ind] == "empty":
                pass
            else:
                break

        # Проверить все поля, находящиеся правее короля
        for current_col_ind in range(king_position[1] - 1, -1, -1):
            if self.pieces_positions[king_position[0]][current_col_ind] == "rook{}".format(1 - self.active_player) or \
                    self.pieces_positions[king_position[0]][current_col_ind] == "queen{}".format(1 - self.active_player):
                return True
            elif self.pieces_positions[king_position[0]][current_col_ind] == "empty":
                pass
            else:
                break

        # Проверить, угрожают ли королю слоны (и королевы по диагональным направлениям)

        # Проверить все поля, находящиеся выше-слева короля
        for offset in range(-1, -1 * min(king_position[0], king_position[1]) - 1, -1):
            if self.pieces_positions[king_position[0] + offset][king_position[1] + offset] == "bishop{}".format(1 - self.active_player) or \
                    self.pieces_positions[king_position[0] + offset][king_position[1] + offset] == "queen{}".format(1 - self.active_player):
                return True
            elif self.pieces_positions[king_position[0] + offset][king_position[1] + offset] == "empty":
                pass
            else:
                break

        # Проверить все поля, находящиеся ниже-справа короля
        for offset in range(-1, -1 * min(7 - king_position[0], 7 - king_position[1]) - 1, -1):
            if self.pieces_positions[king_position[0] - offset][king_position[1] - offset] == "bishop{}".format(1 - self.active_player) or \
                    self.pieces_positions[king_position[0] - offset][king_position[1] - offset] == "queen{}".format(1 - self.active_player):
                return True
            elif self.pieces_positions[king_position[0] - offset][king_position[1] - offset] == "empty":
                pass
            else:
                break

        # Проверить все поля, находящиеся ниже-слева короля
        for offset in range(-1, -1 * min(7 - king_position[0], king_position[1]) - 1, -1):
            if self.pieces_positions[king_position[0] - offset][king_position[1] + offset] == "bishop{}".format(1 - self.active_player) or \
                    self.pieces_positions[king_position[0] - offset][king_position[1] + offset] == "queen{}".format(1 - self.active_player):
                return True
            elif self.pieces_positions[king_position[0] - offset][king_position[1] + offset] == "empty":
                pass
            else:
                break

        # Проверить все поля, находящиеся выше-справа короля
        for offset in range(-1, -1 * min(king_position[0], 7 - king_position[1]) - 1, -1):
            if self.pieces_positions[king_position[0] + offset][king_position[1] - offset] ==\
                    "bishop{}".format(1 - self.active_player) or \
                    self.pieces_positions[king_position[0] + offset][king_position[1] - offset] ==\
                    "queen{}".format(1 - self.active_player):
                return True
            elif self.pieces_positions[king_position[0] + offset][king_position[1] - offset] == "empty":
                pass
            else:
                break

        return False
