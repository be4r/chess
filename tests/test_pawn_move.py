"""Тест корректных движений пешки."""

import unittest
from backend import Board, check_if_move_correct


class PawnMoveTest(unittest.TestCase):
    """Класс, реализующий проверку корректных движений пешки."""

    def setUp(self):
        """Функция, инициализирующая необходимое состояние доски."""
        self.board = Board()

    def test_correct_moves(self):
        """Функция, тестирующая корректные движения пешки."""
        self.assertTrue(check_if_move_correct(self.board, ((6, 4), (5, 4))))
        self.assertTrue(check_if_move_correct(self.board, ((6, 4), (4, 4))))

    def test_incorrect_moves(self):
        """Функция, тестирующая некорректные движения пешки."""
        self.assertFalse(check_if_move_correct(self.board, ((6, 4), (5, 3))))
        self.assertFalse(check_if_move_correct(self.board, ((6, 4), (0, 0))))


if __name__ == "__main__":
    unittest.main()
