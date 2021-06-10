'''
The module that manages frontend: all the drwaings and prettyness

:copyright: (c) copyleft (R), 2021

:license: GNU GPL

'''
import os, sys 
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import backend
import tkinter as tk
import tkinter.font as font
import gettext
#import tkinter.messagebox as msgbox
from threading import Thread
from playsound import playsound as play_sound
from PIL import Image, ImageTk
try:
	from backend import check_if_move_correct, add_move_to_board, check_if_end_of_game, Board
except:
	pass
try:
	from .backend import check_if_move_correct, add_move_to_board, check_if_end_of_game, Board
except:
	pass

grid_size = 96
imgs_path = '%s/imgs' % os.path.dirname(os.path.abspath(__file__))
sound_path = '%s/sound' % os.path.dirname(os.path.abspath(__file__))

gettext.install('chess', localedir = 'po')

def playsound(filename):
	'''
	Plays sound asynchronically (now thats not an easy word sorry for misspelling 2lazy2google)

	:param filename: name of sound file to play

	:return: None
	'''
	return #cos there are problems with sound
	try:
		t = Thread(target = lambda: play_sound("%s/%s" % (sound_path, filename)))
		t.start()
	except:
		pass

class Game(tk.Tk):
	'main class, descendant from tkinter'
	allow_select_pieces = True
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
			font = font.Font(family="Lucida Grande", size=40),text=_('Ходят белые'))
		self.turn_label.place(x = 200, y = 200)
		self.turn_label.grid()
		self.canvas = tk.Canvas(self, height = grid_size * 8, width = grid_size * 8)
		self.canvas.grid()

		# vars
		self.imgs_cache = {}
		self.imgs = []
		self.turn = {'stage': 0, 'x': 0, 'y': 0}
		self.is_check = False

		self.board = Board()
		self.redraw(self.board.get_pieces_positions(), False)

	def redraw(self, board, active):
		'''
		Draw whole board-field

		:param board: matrix of chess figures
		:param active: type `bool`
		
		:return: None
		'''
		# delete old
		for i in self.canvas.find_all():
			self.canvas.delete(i)
		# draw new
		for i, line in enumerate(board):
			for j, piece in enumerate(line):
				self.image_draw(piece, (j, i), active)
				# check
				if piece == 'king%d' % int(self.board.active_player):
					if self.board.check_if_check():
						if not self.is_check:
							playsound('check.mp3')
							self.is_check = True
						# load check img
						self.imgs_cache['check'] = ImageTk.PhotoImage(
								Image.open('%s/%s' % (imgs_path, 'uniq/check.png')).resize((grid_size,grid_size)), size=(grid_size,grid_size))
						self.check_img = self.canvas.create_image(j * grid_size, i * grid_size, 
								image = self.imgs_cache['check'], anchor = 'nw')
						self.canvas.tag_bind(self.check_img, '<Button-1>', lambda e: self.select_tile(e))
					else:
						self.is_check = False
						# self.canvas.delete(self.check_img)
	

	def image_draw(self, piece, coords, active):
		'''
		Draw single piece

		:param piece: Which piece should be drawn
		:param coords: Where should it be drawn
		:param active: Should it highlight onmouseover

		:return: None
		'''
		if not self.imgs_cache.get(piece):
			# if not already cached, load img
			pieces_imgs = {'rook0':'rook_white.png', 'knight0':'knight_white.png', 
				'bishop0':'bishop_white.png', 'king0':'king_white.png', 
				'queen0':'queen_white.png', 'pawn0':'pawn_white.png', 
				'rook1':'rook_black.png', 'knight1':'knight_black.png', 
				'bishop1':'bishop_black.png', 'king1':'king_black.png', 
				'queen1':'queen_black.png', 'pawn1':'pawn_black.png',
				'empty': 'empty.png'}
			piece_orig_img_path = '%s/orig/%s' % (imgs_path, pieces_imgs[piece])
			piece_active_img_path = '%s/selected/%s' % (imgs_path, pieces_imgs[piece])
			img1 = ImageTk.PhotoImage(Image.open(piece_orig_img_path).resize((grid_size,grid_size)), size=(grid_size,grid_size))
			img2 = ImageTk.PhotoImage(Image.open(piece_active_img_path).resize((grid_size,grid_size)), size=(grid_size,grid_size))
			self.imgs_cache[piece] = img1
			self.imgs_cache['%s_selected' % piece] = img2
		# draw cached
		if active:
			piece_img = self.canvas.create_image(coords[0] * grid_size, coords[1] * grid_size, 
					anchor='nw',image = self.imgs_cache[piece], activeimage = self.imgs_cache['%s_selected' % piece])
		else:
			piece_img = self.canvas.create_image(coords[0] * grid_size, coords[1] * grid_size, 
					anchor='nw',image = self.imgs_cache[piece])
		self.imgs.append(piece)
		# bind onclick event
		self.canvas.tag_bind(piece_img, '<Button-1>', lambda e: self.select_tile(e))
		self.canvas.grid()

	def pawn_change_ask(self, pos):
		'''
		When pawn reaches most distant line (1 for white and 8 for black), it should be changed into another figure. This visualises `dialog popup` to interract with user on this topic.
		:param pos: Which pawn is changing
		:return: None
		'''
		self.allow_select_pieces = False
		# graphical stuff
		self.turn_label.configure(text =  _('Выберите фигуру:'))
		sizes = (6 * grid_size, 2 * grid_size)
		self.imgs_cache['choose'] = ImageTk.PhotoImage(Image.open('%s/%s' % (imgs_path, 'uniq/choose.png')).resize(sizes), size = sizes)
		self.canvas.create_image(1 * grid_size, 3 * grid_size, image = self.imgs_cache['choose'], anchor='nw')
		q = 0 if self.board.active_player else 1
		queen = self.canvas.create_image(1.25 * grid_size, 3.5 * grid_size, image = self.imgs_cache['queen%d' % q], anchor = 'nw')
		bishop = self.canvas.create_image(2.75 * grid_size, 3.5 * grid_size, image = self.imgs_cache['bishop%d' % q], anchor = 'nw')
		knight = self.canvas.create_image(4.25 * grid_size, 3.5 * grid_size, image = self.imgs_cache['knight%d' % q], anchor = 'nw')
		rook = self.canvas.create_image(5.75 * grid_size, 3.5 * grid_size, image = self.imgs_cache['rook%d' % q], anchor = 'nw')
		# callback on figure choice
		def set_answer(answer):
			'''
			Subfunction for returning which piece was chosen by user.
			:param answer: Its the piece name
			'''
			for i in self.canvas.find_all()[-5:]:
				self.canvas.delete(i)
			self.turn_label.configure(text = _('Ходят белые') if not self.board.active_player else _('Ходят черные'))
			self.allow_select_pieces = True
			self.board.change_pawn(pos, answer)
			# redraw
			self.redraw(self.board.get_pieces_positions(), False)
			print(answer, pos)
		# veshayem callback
		self.canvas.tag_bind(queen, '<Button-1>', lambda e: set_answer('queen'))
		self.canvas.tag_bind(bishop, '<Button-1>', lambda e: set_answer('bishop'))
		self.canvas.tag_bind(knight, '<Button-1>', lambda e: set_answer('knight'))
		self.canvas.tag_bind(rook, '<Button-1>', lambda e: set_answer('rook'))

	def end_game(self, end_type):
		'''
		Ends the game: pretty win/lose img, sound, stops user interaction

		:param ent_type: How did it end? (White checkmate / black checkmate / stalemate)
		'''
		print('WIN!')
		self.allow_select_pieces = False
		if end_type == 'checkmate0':
			self.imgs_cache['win'] = ImageTk.PhotoImage(
					Image.open(_('%s/uniq/winRU.png' % imgs_path)).resize(
					(grid_size * 8, grid_size * 8)), size=(grid_size * 8, grid_size * 8))
			piece_img = self.canvas.create_image(4 * grid_size, 4 * grid_size, image = self.imgs_cache['win'])
			print(_('imgs/uniq/winRU.png'))
			self.canvas.grid()
			self.turn_label.configure(text = _('Победа!'))
			playsound('win.mp3')
		elif end_type == 'checkmate1':
			self.imgs_cache['lose'] = ImageTk.PhotoImage(
					Image.open(_('%s/uniq/loseRU.png' % imgs_path)).resize(
					(grid_size * 8, grid_size * 8)), size=(grid_size * 8, grid_size * 8))
			piece_img = self.canvas.create_image(4 * grid_size, 4 * grid_size, image = self.imgs_cache['lose'])
			self.turn_label.configure(text = _('Поражение . . . . . . . '))
			playsound('lose.mp3')
		else: # stalemate
			self.imgs_cache['stale'] = ImageTk.PhotoImage(
					Image.open(_('%s/uniq/pat.png' % imgs_path)).resize(
					(grid_size * 8, grid_size * 8)), size=(grid_size * 8, grid_size * 8))
			piece_img = self.canvas.create_image(4 * grid_size, 4 * grid_size, image = self.imgs_cache['stale'])
			self.turn_label.configure(text = _('Патовая ситуация'))
			playsound('pat.mp3')
			

	def select_tile(self, event):
		'''
		This happend when user has clicked somewhere on the board, preferably on one of his figures
		:param event: Mouse click event
		'''
		if self.allow_select_pieces == False:
			playsound('error.mp3')
			return
		if self.turn['stage'] == 0:
			# if its first click
			# get tile number from coords
			x = self.turn['x'] = event.x // grid_size
			y = self.turn['y'] = event.y // grid_size
			# mark selected
			# if selected white on black turn or other side around
			if (((self.board.get_pieces_positions()[y][x][-1] != '0') and not self.board.active_player)
				or ((self.board.get_pieces_positions()[y][x][-1] != '1') and self.board.active_player)):
				print('wrong color')
				return
			playsound('press1.mp3')
			self.turn['stage'] = 1
			self.redraw(self.board.get_pieces_positions(), True)
			self.imgs_cache['selection'] = ImageTk.PhotoImage(
					Image.open('%s/uniq/select1.png' % imgs_path).resize((grid_size,grid_size)), size=(grid_size,grid_size))
			self.selection_img = self.canvas.create_image(x * grid_size, y * grid_size, image = self.imgs_cache['selection'], anchor = 'nw')
		elif self.turn['stage'] == 1:
			self.canvas.delete(self.selection_img)
			# if its second click, send MOVE to backend
			self.turn['stage'] = 0
			move = ((self.turn['y'], self.turn['x']),  (event.y // grid_size, event.x // grid_size))
			print('trying ', move)

			pawn_pos = None
			if check_if_move_correct(self.board, move):
				# made move successfull
				self.turn_label.configure(text = _('Ходят белые') if self.board.active_player else _('Ходят черные'))
				playsound('press2.mp3')
				pawn_pos = add_move_to_board(self.board, move)
			else:
				# incorrect move
				playsound('error.mp3')
				# msgbox.showerror(title='ATTENTION!', message='This move is prohibited!\nIts impossible!\n\nYOU DID BAD!')
			is_ended, end_type =  check_if_end_of_game(self.board, move)
			if is_ended:
				self.end_game(end_type)
			else:
				# redraw and stuff
				self.redraw(self.board.get_pieces_positions(), False)
			if pawn_pos:
				answer = self.pawn_change_ask(pawn_pos)
		pass


	def start(self):
		'''
		Start the game. Takes no parameters, returns nothing
		'''
		self.mainloop()

if __name__ == '__main__':
	game = Game()
	game.start()