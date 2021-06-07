import tkinter as tk
from PIL import Image, ImageTk
#from backend import check_if_move_correct, add_move_to_board, check_if_end_of_game, Board

grid_size = 64

class Game(tk.Tk):
	def __init__(self):
		super().__init__()
		for i in range(8):
			self.rowconfigure(i, weight=1)
			self.columnconfigure(i, weight=1)
		self.minsize(512,512)

		self.canvas = tk.Canvas(self, height = 512, width = 512)
		self.canvas.grid()
		self.frame = tk.Frame(self)
		self.frame.grid()

		self.imgs = []

		#self.board = Board()
		board = [['rook0', 'knight0', 'bishop0', 'king0', 'queen0', 'bishop0', 'knight0', 'rook0'], 
			['pawn0', 'pawn0', 'pawn0', 'pawn0', 'pawn0', 'pawn0', 'pawn0', 'pawn0'], 
			*[['e'] * 8]*4, 
			['pawn1', 'pawn1', 'pawn1', 'pawn1', 'pawn1', 'pawn1', 'pawn1', 'pawn1'], 
			['rook1', 'knight1', 'bishop1', 'king1', 'queen1', 'bishop1', 'knight1', 'rook1']]
		self.redraw(board)

	def redraw(self, board):
		for i, line in enumerate(board):
			for j, piece in enumerate(line):
				self.draw(piece, (j, i))
		self.mainloop()

	def draw(self, piece, coords):
		pieces_imgs = {'rook0':'rook_white.png', 'knight0':'knight_white.png', 
			'bishop0':'bishop_white.png', 'king0':'king_white.png', 
			'queen0':'queen_white.png', 'pawn0':'pawn_white.png', 
			'rook1':'rook_black.png', 'knight1':'knight_black.png', 
			'bishop1':'bishop_black.png', 'king1':'king_black.png', 
			'queen1':'queen_black.png', 'pawn1':'pawn_black.png',
			'e': 'empty.png'}
		piece_img = 'imgs/%s' % pieces_imgs[piece]
		img = ImageTk.PhotoImage(Image.open(piece_img).resize((100,100)), size=(100,100))
		self.imgs.append(img)
		self.canvas.create_image(coords[0] * grid_size, coords[1] * grid_size, anchor='nw',image=img)
		self.canvas.grid()

	def make_move(self):
		pass


	def start(self):
		self.mainloop()
'''
		while True:
			show_board()
			move = get_move()
			if check_if_move_correct(self.board, move):
				add_move_to_board(self.board, move)
			else:
				print("You wanna do wrong thing! It's not possible.")
			if check_if_end_of_game(self.board, move):
				end_game()
'''

game = Game()
game.mainloop()
game.start()
