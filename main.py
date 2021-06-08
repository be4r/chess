'''
The module that manages frontend: all the drwaings and prettyness
:copyright: (c) copyleft (R), 2021
:license: GNU GPL
'''

import tkinter as tk
import tkinter.messagebox as msgbox
from PIL import Image, ImageTk
#from backend import check_if_move_correct, add_move_to_board, check_if_end_of_game, Board

grid_size = 128

class Board():
	def get_pieces_positions(self):
		return [['rook0', 'knight0', 'bishop0', 'king0', 'queen0', 'bishop0', 'knight0', 'rook0'], 
			['pawn0', 'pawn0', 'pawn0', 'pawn0', 'pawn0', 'pawn0', 'pawn0', 'pawn0'], 
			*[['empty'] * 8]*4, 
			['pawn1', 'pawn1', 'pawn1', 'pawn1', 'pawn1', 'pawn1', 'pawn1', 'pawn1'], 
			['rook1', 'knight1', 'bishop1', 'king1', 'queen1', 'bishop1', 'knight1', 'rook1']]

class Game(tk.Tk):
	'main class, descendant from tkinter'
	def __init__(self):
		'''
		Constructor
		:param self: because this is methor
		:return: idk nothing
		'''
		super().__init__()
		for i in range(8):
			self.rowconfigure(i, weight=1)
			self.columnconfigure(i, weight=1)
		self.minsize(*(grid_size * 8,)*2)

		self.canvas = tk.Canvas(self, height = grid_size * 8, width = grid_size * 8)
		self.canvas.grid()
		self.frame = tk.Frame(self)
		self.frame.grid()

		self.imgs_cache = {}
		self.imgs = []
		self.turn = {'stage': 0, 'x': 0, 'y': 0}

		self.board = Board()
		self.redraw(self.board.get_pieces_positions(), False)

	def redraw(self, board, active):
		'''
		Redrawd board-field

		:param board: matrix of chess figures
		:param active: type `bool`
		'''
		# idk where to put next 3 lines :D
		if 'empty2' not in self.imgs_cache:
			img = ImageTk.PhotoImage(Image.open('imgs/empty2.png').resize((grid_size,grid_size)), size=(grid_size,grid_size))
			self.imgs_cache['empty2'] = img
		# delete old
		for i in self.canvas.find_all():
			self.canvas.delete(i)
		# draw new
		for i, line in enumerate(board):
			for j, piece in enumerate(line):
				self.image_draw(piece, (j, i), active)

	def image_draw(self, piece, coords, active):
		if not self.imgs_cache.get(piece):
			# if not already cached, load img
			pieces_imgs = {'rook0':'rook_white.png', 'knight0':'knight_white.png', 
				'bishop0':'bishop_white.png', 'king0':'king_white.png', 
				'queen0':'queen_white.png', 'pawn0':'pawn_white.png', 
				'rook1':'rook_black.png', 'knight1':'knight_black.png', 
				'bishop1':'bishop_black.png', 'king1':'king_black.png', 
				'queen1':'queen_black.png', 'pawn1':'pawn_black.png',
				'empty': 'empty.png'}
			piece_img_path = 'imgs/%s' % pieces_imgs[piece]
			img = ImageTk.PhotoImage(Image.open(piece_img_path).resize((grid_size,grid_size)), size=(grid_size,grid_size))
			self.imgs_cache[piece] = img
		# draw cached
		if active:
			piece_img = self.canvas.create_image(coords[0] * grid_size, coords[1] * grid_size, anchor='nw',image = self.imgs_cache[piece], activeimage = self.imgs_cache['empty2'])
		else:
			piece_img = self.canvas.create_image(coords[0] * grid_size, coords[1] * grid_size, anchor='nw',image = self.imgs_cache[piece])
		self.imgs.append(piece)
		# bind onclick event
		self.canvas.tag_bind(piece_img, '<Button-1>', lambda e: self.select_tile(e))
		self.canvas.grid()

	

	def select_tile(self, event):
		if self.turn['stage'] == 0:
			# if its first click
			# get tile number from coords
			self.turn['x'] = event.x // grid_size
			self.turn['y'] = event.y // grid_size
			self.turn['stage'] = 1
			self.redraw(self.board.get_pieces_positions(), True)
		elif self.turn['stage'] == 1:
			# if its second click, send MOVE to backend
			self.turn['stage'] = 0
			move = ((self.turn['y'], self.turn['x']),  (event.y // grid_size, event.x // grid_size))
			print('trying ', move)
			# TODO: as backend gets implemented, add this
			#if check_if_move_correct(self.board, move):
			#	add_move_to_board(self.board, move)
			#else:
				# incorrect move
			msgbox.showerror(title='ATTENTION!', message='This move is prohibited!\nIts impossible!\n\nYOU DID BAD!')
			#if check_if_end_of_game(self.board, move):
			#	end_game()
			self.redraw(self.board.get_pieces_positions(), False)
		pass


	def start(self):
		self.mainloop()

game = Game()
game.start()
