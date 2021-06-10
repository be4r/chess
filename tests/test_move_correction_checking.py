"""Тест функции, проверяющей корректность хода."""

import unittest
from backend import Board, check_if_move_correct, add_move_to_board


class MoveCheckFunctionTest(unittest.TestCase):
    """Класс, реализующий проверку функции проверки корректности хода."""

    def setUp(self):
        """Функция, инициализирующая необходимое состояние доски."""
        self.board = Board()

    def test_pawn_moves(self):
        """Функция, тестирующая возможные и невозможные ходы пешки."""
        self.assertTrue(check_if_move_correct(self.board, ((6, 4), (5, 4))))
        self.assertTrue(check_if_move_correct(self.board, ((6, 4), (4, 4))))
        self.assertFalse(check_if_move_correct(self.board, ((6, 4), (5, 3))))
        self.assertFalse(check_if_move_correct(self.board, ((6, 4), (0, 0))))

    def test_rook_moves(self):
        """Функция, тестирующая возможные и невозможные ходы ладьи."""
        self.assertFalse(check_if_move_correct(self.board, ((7, 0), (7, 1))))
        add_move_to_board(self.board, ((7, 1), (5, 0)))
        self.assertFalse(check_if_move_correct(self.board, ((7, 0), (7, 1))))
        add_move_to_board(self.board, ((1, 0), (2, 0)))
        self.assertTrue(check_if_move_correct(self.board, ((7, 0), (7, 1))))


if __name__ == "__main__":
    unittest.main()
