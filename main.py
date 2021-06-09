'''
The module that manages frontend: all the drwaings and prettyness
:copyright: (c) copyleft (R), 2021
:license: GNU GPL
'''

import tkinter as tk
import tkinter.font as font
import tkinter.messagebox as msgbox
from playsound import playsound
from PIL import Image, ImageTk
from backend import check_if_move_correct, add_move_to_board, check_if_end_of_game, Board

grid_size = 96
turn_black = False

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

		self.frame = tk.Frame(self)
		self.frame.grid()
		self.turn_label = tk.Label(self.frame, relief = tk.RAISED, 
			font = font.Font(family="Lucida Grande", size=40),text='Ходят белые')
		self.turn_label.place(x = 200, y = 200)
		self.turn_label.grid()
		self.canvas = tk.Canvas(self, height = grid_size * 8, width = grid_size * 8)
		self.canvas.grid()

		# vars
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

	def make_move(self, move):
		global turn_black
		turn_black = not turn_black
		self.turn_label.configure(text = 'Ходят черные' if turn_black else 'Ходят белые')
		playsound('sound/press2.mp3')
		pawn_pos = add_move_to_board(self.board, move)
		if pawn_pos:
			answer = self.pawn_change_ask(pos)
			self.board.change_pawn(pawn_pos, answer)
	
	def pawn_change_ask(self, pos):
		sizes = (6 * grid_size, 2 * grid_size)
		self.choose_image = ImageTk.PhotoImage(Image.open('imgs/choose.png').resize(sizes), size = sizes)
		self.canvas.create_image(1 * grid_size, 3 * grid_size, image = self.choose_image, anchor='nw')
		queen = self.canvas.create_image(1.25 * grid_size, 3.5 * grid_size, image = self.imgs_cache['queen0'], anchor = 'nw')
		bishop = self.canvas.create_image(2.75 * grid_size, 3.5 * grid_size, image = self.imgs_cache['bishop0'], anchor = 'nw')
		knight = self.canvas.create_image(4.25 * grid_size, 3.5 * grid_size, image = self.imgs_cache['knight0'], anchor = 'nw')
		rook = self.canvas.create_image(5.75 * grid_size, 3.5 * grid_size, image = self.imgs_cache['rook0'], anchor = 'nw')
		def set_answer(answer):
			for i in self.canvas.find_all()[-5:]:
				self.canvas.delete(i)
			print(answer, pos)
		self.canvas.tag_bind(queen, '<Button-1>', lambda e: set_answer('queen'))
		self.canvas.tag_bind(bishop, '<Button-1>', lambda e: set_answer('bishop'))
		self.canvas.tag_bind(knight, '<Button-1>', lambda e: set_answer('knight'))
		self.canvas.tag_bind(rook, '<Button-1>', lambda e: set_answer('rook'))

	def end_game(self, end_type):
		end_img = ImageTk.PhotoImage(Image.open('imgs/mate.png').resize((grid_size * 8,grid_size * 8)), size=(grid_size * 8,grid_size * 8))
		piece_img = self.canvas.create_image(0, 0, anchor='nw',image = end_img)

	def select_tile(self, event):
		if self.turn['stage'] == 0:
			playsound('sound/press1.mp3')
			# if its first click
			# get tile number from coords
			self.turn['x'] = event.x // grid_size
			self.turn['y'] = event.y // grid_size
			# if selected white on black turn or other side around
			if (self.board.get_pieces_positions()[self.turn['x']][self.turn['y']][-1] == '1') ^ turn_black:
				print('wrong color')
				return
			self.turn['stage'] = 1
			self.redraw(self.board.get_pieces_positions(), True)
		elif self.turn['stage'] == 1:
			# if its second click, send MOVE to backend
			self.turn['stage'] = 0
			move = ((self.turn['y'], self.turn['x']),  (event.y // grid_size, event.x // grid_size))
			print('trying ', move)

			if check_if_move_correct(self.board, move):
				# made move successfull
				self.make_move(move)
			else:
				# incorrect move
				playsound('sound/error.mp3')
				# msgbox.showerror(title='ATTENTION!', message='This move is prohibited!\nIts impossible!\n\nYOU DID BAD!')
			is_ended, end_type =  check_if_end_of_game(self.board, move)
			if is_ended:
				self.end_game(end_type)
			# redraw and stuff
			self.redraw(self.board.get_pieces_positions(), False)
			self.pawn_change_ask((0,0))
		pass


	def start(self):
		self.mainloop()

game = Game()
game.start()
