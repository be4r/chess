import unittest
from backend import Board, check_if_move_correct, add_move_to_board


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        
    
    def test_initial_state(self):
        self.assertFalse(self.board.check_if_check())

    def test_fast_check(self):
        add_move_to_board(self.board, ((6, 3), (5, 3)))
        add_move_to_board(self.board, ((1, 2), (2, 2)))
        add_move_to_board(self.board, ((7, 6), (5, 5)))
        add_move_to_board(self.board, ((0, 3), (3, 0)))        

        self.assertTrue(self.board.check_if_check())
    

if __name__ == "__main__":
    unittest.main()



