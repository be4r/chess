"""Тест функции, вычисляющей возможные ходы фигур."""

import unittest
from backend import Board, add_move_to_board


class CheckMateTest(unittest.TestCase):
    """Класс, реализующий проверку функции, вычисляющей возможные ходы фигур."""

    def setUp(self):
        """Функция, инициализирующая необходимое состояние доски."""
        self.board = Board()

    def test_initial_state_pawn1(self):
        """Функция, проверяющая корректность вычисляемых ходов для чёрной пешки."""
        true_pawn_possible_moves = [((1, 1), (0, 2)), ((1, 1), (0, 0))]
        self.assertEqual(self.board.get_pawn_possible_moves(1, 1), true_pawn_possible_moves)

    def test_initial_state_pawn0(self):
        """Функция, проверяющая корректность вычисляемых ходов для белой пешки."""
        true_pawn_possible_moves = [((6, 4), (5, 4)), ((6, 4), (4, 4))]
        self.assertEqual(self.board.get_pawn_possible_moves(6, 4), true_pawn_possible_moves)

    def test_fast_mate_moves(self):
        """Функция, проверяющая, что после мата нет корректных ходов."""
        add_move_to_board(self.board, ((6, 6), (4, 6)))
        add_move_to_board(self.board, ((1, 4), (2, 4)))
        add_move_to_board(self.board, ((6, 5), (5, 5)))
        add_move_to_board(self.board, ((0, 3), (4, 7)))

        self.assertEqual(self.board.get_all_possible_moves(), [])


if __name__ == "__main__":
    unittest.main()
