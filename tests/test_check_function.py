"""Тест шаха."""

import unittest
from chess.backend import Board, add_move_to_board


class CheckTest(unittest.TestCase):
    """Класс, реализующий проверку теста шаха."""

    def setUp(self):
        """Функция, инициализирующая необходимое состояние доски."""
        self.board = Board()

    def test_initial_state(self):
        """Функция, тестирующая возможность шаха в начальном состоянии доски."""
        self.assertFalse(self.board.check_if_check())

    def test_fast_check(self):
        """Функция, тестирующая возможность шаха в состоянии доски, на которой стоит мат."""
        add_move_to_board(self.board, ((6, 3), (5, 3)))
        add_move_to_board(self.board, ((1, 2), (2, 2)))
        add_move_to_board(self.board, ((7, 6), (5, 5)))
        add_move_to_board(self.board, ((0, 3), (3, 0)))

        self.assertTrue(self.board.check_if_check())


if __name__ == "__main__":
    unittest.main()
