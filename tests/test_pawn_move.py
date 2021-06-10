import unittest
from backend import Board, check_if_move_correct

class PawnMoveTest(unittest.TestCase):
    def setUp(self):
        self.board = Board()
    
    def test_correct_moves(self):
        self.assertTrue(check_if_move_correct(self.board, ((6, 4),(5, 4)) ))
        self.assertTrue(check_if_move_correct(self.board, ((6, 4),(4, 4)) ))
    
    def test_incorrect_moves(self):
        self.assertFalse(check_if_move_correct(self.board, ((6, 4), (5, 3)) ))
        self.assertFalse(check_if_move_correct(self.board, ((6, 4), (0, 0)) ))

if __name__ == "__main__":
    unittest.main()



