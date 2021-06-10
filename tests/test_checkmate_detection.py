import unittest
from backend import Board, add_move_to_board, check_if_end_of_game


class CheckMateTest(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        
    
    def test_initial_state(self):
        self.assertFalse(check_if_end_of_game(self.board, ((0, 0), (0, 0)) )[0])

    def test_fast_mate_state(self):
        add_move_to_board(self.board, ((6, 6), (4, 6)) )
        add_move_to_board(self.board, ((1, 4), (2, 4)) )
        add_move_to_board(self.board, ((6, 5), (5, 5)) )
        add_move_to_board(self.board, ((0, 3), (4, 7)) )

        is_end = check_if_end_of_game(self.board, None)
        print(is_end)
        self.assertTrue(is_end[0])
        self.assertEqual(is_end[1][:-1], "checkmate")

if __name__ == "__main__":
    unittest.main()



