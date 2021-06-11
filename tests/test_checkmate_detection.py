"""Тест обнаружения мата на доске."""

import unittest
from chess.backend import Board, add_move_to_board, check_if_end_of_game


class CheckMateTest(unittest.TestCase):
    """Класс, реализующий проверку теста обнаружения мата."""

    def setUp(self):
        """Функция, инициализирующая необходимое состояние доски."""
        self.board = Board()

    def test_initial_state(self):
        """Функция, тестирующая возможность мата в начальном состоянии доски."""
        self.assertFalse(check_if_end_of_game(self.board, ((0, 0), (0, 0)))[0])

    def test_fast_mate_state(self):
        """Функция, тестирующая возможность мата в состоянии доски, на которой стоит мат."""
        add_move_to_board(self.board, ((6, 6), (4, 6)))
        add_move_to_board(self.board, ((1, 4), (2, 4)))
        add_move_to_board(self.board, ((6, 5), (5, 5)))
        add_move_to_board(self.board, ((0, 3), (4, 7)))

        is_end = check_if_end_of_game(self.board, None)
        print(is_end)
        self.assertTrue(is_end[0])
        self.assertEqual(is_end[1][:-1], "checkmate")


if __name__ == "__main__":
    unittest.main()
