# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.widget import Widget
from tetriscore import SparseGridLayout,GridEntry
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, NumericProperty,ListProperty, BooleanProperty,Property
import random
from pieces import *
from kivy.clock import Clock
from kivy.core.window import Keyboard
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.core.audio import SoundLoader
from kivy.utils import platform
from functools import partial

key_vectors = {
    'up': (0, 1),
    'right': (1, 0),
    'down': (0, -1),
    'left': (-1, 0),
	'spacebar':(0,0),
}

class TetrisManager(ScreenManager):

	def __init__(self, *args, **kwargs):
		super(TetrisManager, self).__init__(*args, **kwargs)
		self.add_widget(MainScreen())

	def start_tetris(self):
		if self.has_screen('tetris'):
			self.remove_widget(self.get_screen('tetris'))
		self.add_widget(TetrisScreen())
		self.current = 'tetris'

class MainScreen(Screen):
    pass

class TetrisScreen(Screen):
	tetris = ObjectProperty() 
	left_button = ObjectProperty() 
	right_button = ObjectProperty() 
	up_button = ObjectProperty() 
	down_button = ObjectProperty()
	moving_faster = BooleanProperty(False)
	def __init__(self, **kwargs):
		super(TetrisScreen, self).__init__(**kwargs)
		self.get_platform()
	
	def create_clock(self,dir_x,dir_y,touch):
		#print 'click'
		#print touch 
		callback = partial(self.tetris.move_fast,dir_x,dir_y,touch)
		Clock.schedule_once(callback, .5)
		touch.ud['event'] = callback

	def delete_clock(self,touch):
		if self.moving_faster:
			Clock.unschedule(touch.ud['event'])
			self.moving_faster=False
		if self.tetris.is_moving_fast:
			Clock.unschedule(touch.ud['moving'])
			self.tetris.is_moving_fast=False
	def on_touch_down(self,touch):
		#print touch.pos
		if self.left_button.collide_point(*touch.pos):
			self.create_clock(-1,0,touch)
			self.moving_faster=True
		if self.right_button.collide_point(*touch.pos):
			self.create_clock(1,0,touch)
			self.moving_faster=True
		if self.up_button.collide_point(*touch.pos):
			self.create_clock(0,1,touch)
			self.moving_faster=True
		if self.down_button.collide_point(*touch.pos):
			self.create_clock(0,-1,touch)
			self.moving_faster=True
		return super(TetrisScreen, self).on_touch_down(touch)
	def on_touch_up(self,touch):
		self.delete_clock(touch)
	def on_size(self,x,y):
		if self.width*.7 > self.height*.5:
			self.tetris.size_hint=(None,1)
			self.tetris.width=self.height*.5
		else:
			self.tetris.size_hint=(1,None)
			self.tetris.height=self.width*2*.7
		#print self.tetris.size
	

	def get_platform(self):
		direction=self.ids.direction
		#print platform
		if platform == 'linux' or platform == 'win':
			direction.opacity=1
			self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
			self._keyboard.bind(on_key_down=self._on_keyboard_down)
		else:
			direction.opacity=1
			
		#self.remove_widget(direction)
		#self.add_widget(direction)   
	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		
		if keycode[1] in key_vectors and not self.tetris.game_over:
			self.tetris.move(*key_vectors[keycode[1]])
class Tetris_piece(SparseGridLayout):
	pieces = ListProperty(['I', 'J', 'L', 'O', 'S', 'T', 'Z'])
	piece_num = NumericProperty(None)
	show_piece = ObjectProperty(None)
	last_piece = ObjectProperty(None)
	def __init__(self, **kwargs):
		super(Tetris_piece, self).__init__(**kwargs)
		
		#self.add_widget(self.next_piece)
	def on_piece_num(self,*args,**kagrs):
		if self.last_piece:
			self.release_piece()
		#print 'show_piece'
		self.show_piece = Piece.factory(self.pieces[self.piece_num])
		#self.remove_widget(self.show_piece)
		self.show_piece.release_bricks()
		self.show_piece.row = 3
		self.show_piece.column = 1
		for brick in self.show_piece.bricks:
			# set positioning of brick to align to grid
			pos = brick.pos_hint
			brick.row = self.show_piece.row + pos['y']
			brick.column = self.show_piece.column + pos['x']
			self.add_widget(brick)
			#self.remove_widget(brick)
		#\self.add_widget(show_piece)
		self.last_piece = self.show_piece
	def release_piece(self):
		for brick in self.last_piece.bricks:
			# set positioning of brick to align to grid
			pos = brick.pos_hint
			brick.row = self.last_piece.row + pos['y']
			brick.column = self.last_piece.column + pos['x']
			#self.add_widget(brick)
			self.remove_widget(brick)
class Tetris(SparseGridLayout):
	pieces = ListProperty(['I', 'J', 'L', 'O', 'S', 'T', 'Z'])
	next_piece = ObjectProperty(None)
	falling_piece = ObjectProperty(None)
	lines = NumericProperty(0)
	points = NumericProperty(0)
	level = NumericProperty(50.0)
	game_over = BooleanProperty(False)
	is_moving_fast = BooleanProperty(False)
	brick_wall = ListProperty([[]] * 22)
	sound = SoundLoader.load('tetris.wav')
	piece_num	= NumericProperty(0)
	def __init__(self, **kwargs):
		super(Tetris, self).__init__(**kwargs)
		#self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		#self._keyboard.bind(on_key_down=self._on_keyboard_down)
		self.sound.loop = True
		self.sound.play()
		self.set_next()
		self.set_falling()
	
	#def _keyboard_closed(self):
	#	self._keyboard.unbind(on_key_down=self._on_keyboard_down)
	#	self._keyboard = None

	#def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
	#	
	#	if keycode[1] in key_vectors and not self.game_over:
	#		self.move(*key_vectors[keycode[1]])
	
	def on_touch_up(self, touch):
		v = Vector(touch.pos) - Vector(touch.opos)
		if v.length() < 20:
			return

		if abs(v.x) > abs(v.y):
			v.y = 0
		else:
			v.x = 0
		if not self.game_over:
			self.move(*v.normalize())
	def move(self, dir_x, dir_y):
		dir_x = int(dir_x)
		dir_y = int(dir_y)
		if dir_x==-1 and not self.collide_falling_left():	
			self.falling_piece.strifel()
		elif dir_x==1 and not self.collide_falling_right():
			self.falling_piece.strifer()
		elif dir_y==1 and not self.collide_shift():
			self.falling_piece.shift_right()
		elif dir_y==-1:
			self.drop_falling()
		elif dir_x==0 and dir_y == 0:
			self.drop_falling_fast()

	def move_fast_2(self,dir_x,dir_y,args):
		dir_x = int(dir_x)
		dir_y = int(dir_y)
		if dir_x==-1 and not self.collide_falling_left():	
			self.falling_piece.strifel()
		elif dir_x==1 and not self.collide_falling_right():
			self.falling_piece.strifer()
		elif dir_y==1 and not self.collide_shift():
			self.falling_piece.shift_right()
		elif dir_y==-1:
			self.drop_falling()
		
	
	def move_fast(self,dir_x,dir_y,touch,args):
		callback = partial(self.move_fast_2,dir_x,dir_y)
		Clock.schedule_interval(callback,0.2)
		touch.ud['moving'] = callback
		self.is_moving_fast=True
		
	
	def set_falling(self):
		if self.falling_piece:
			self.get_bricks()
		self.falling_piece = self.next_piece
		self.falling_piece.row = 19
		self.falling_piece.column = 5
		self.add_widget(self.falling_piece)
		if self.collide_on_start():
			self.game_over = True
		else:
			Clock.schedule_interval(self.drop_falling, (1 - (self.level / 100)))
			self.set_next()
	def clear_falling(self):
		self.remove_widget(self.falling_piece)
		self.falling_piece.release_bricks()
			
	def get_bricks(self):
		self.clear_falling()
		for brick in self.falling_piece.bricks:
			# set positioning of brick to align to grid
			pos = brick.pos_hint
			brick.row = self.falling_piece.row + pos['y']
			brick.column = self.falling_piece.column + pos['x']
			self.another_brick_in_the_wall(brick)
			self.add_widget(brick)
		self.collapse_wall()
	def set_next(self):
		# generates random next piece to fall
		self.piece_num=random.randint(0, 6)
		random_name = self.pieces[self.piece_num]
		self.next_piece = Piece.factory(random_name)
	def drop_falling_fast(self, *args, **kwargs):
		Clock.schedule_interval(self.drop_falling, .005)
	def drop_falling(self, *args, **kwargs):
		if self.collide_falling():
			Clock.unschedule(self.drop_falling)
			self.set_falling()
		else:
			self.falling_piece.fall()

	def collide_falling(self):
		# checks if falling piece has collided with bottom
		# or fallen over any brick on the wall
		for brick in self.falling_piece.bricks:
			pos = brick.pos_hint
			if self.falling_piece.row + pos['y'] <= 0:
				return True
			anchor_pos = self.falling_piece.grid_pos
			fall_pos = [anchor_pos[0] + pos['y'] - 1,
						anchor_pos[1] + pos['x']]
			if self.brick_wall[fall_pos[0]]:
				if self.brick_wall[fall_pos[0]][fall_pos[1]]:
					return True
	def collide_falling_left(self):
		for brick in self.falling_piece.bricks:
			pos = brick.pos_hint
			pos_x = pos['x'] + self.falling_piece.column
			if (pos_x <= 0):
				return True
			anchor_pos = self.falling_piece.grid_pos
			fall_pos = [anchor_pos[0] + pos['y'],
						anchor_pos[1] + pos['x'] - 1]
			if self.brick_wall[fall_pos[0]]:
				if self.brick_wall[fall_pos[0]][fall_pos[1]]:
					return True
	def collide_falling_right(self):
		# checks if falling piece is touching any piece to its right
		for brick in self.falling_piece.bricks:
			pos = brick.pos_hint
			pos_x = pos['x'] + self.falling_piece.column
			if (pos_x >= 9):
				return True
			anchor_pos = self.falling_piece.grid_pos
			fall_pos = [anchor_pos[0] + pos['y'],
						anchor_pos[1] + pos['x']+1]
			if self.brick_wall[fall_pos[0]]:
				if self.brick_wall[fall_pos[0]][fall_pos[1]]:
					return True
	def collide_shift(self):
		# checks if falling piece will collide if shifted
		for brick in self.falling_piece.bricks:
			pos = brick.pos_hint
			anchor_pos = self.falling_piece.grid_pos
			shift_pos = [anchor_pos[0] + pos['x'],
						 anchor_pos[1] + pos['y']]
			if shift_pos[1] < 0 or shift_pos[1] >= 10 or shift_pos[0]>19:
				return True
			if self.brick_wall[shift_pos[0]]:
				if self.brick_wall[shift_pos[0]][shift_pos[1]]:
					return True

	def another_brick_in_the_wall(self, brick):
		# adds a brick to the wall
		if not self.brick_wall[brick.grid_pos[0]]:
			self.brick_wall[brick.grid_pos[0]] = [None] * 10
		self.brick_wall[brick.grid_pos[0]][brick.grid_pos[1]] = brick
	def collapse_wall(self, *args, **kwargs):
		# checks if any lines in the wall are full
		lines = 0
		for line in reversed(self.brick_wall):
			if line and None not in line:
				for brick in line:
				    self.remove_widget(brick)
				# remove full lines
				self.brick_wall.remove(line)
				self.brick_wall.append([])
				# update score
				lines = lines + 1
				self.points = self.points + 100 * lines * self.level
			self.lines = self.lines + lines
		# updates positioning of blocks in flield (move unfilled lines down)
		for i, line in enumerate(self.brick_wall):
			for brick in line:
				if hasattr(brick, 'row'):
				    brick.row = i
		pass
	def on_lines(self, *args, **kwargs):
		if self.lines % 5 == 0:
			self.level = self.level + 1
	def collide_on_start(self):
		for brick in self.falling_piece.bricks:
		    pos = brick.pos_hint
		    anchor_pos = self.falling_piece.grid_pos
		    fall_pos = [anchor_pos[0] + pos['y'],
		                anchor_pos[1] + pos['x']]
		    if self.brick_wall[fall_pos[0]]:
		        if self.brick_wall[fall_pos[0]][fall_pos[1]]:
		            return True
class TetrisApp(App):
	def build(self):
		return TetrisManager()
	def on_pause(self):
		return True
	def on_resume(self):
		pass
if __name__=='__main__':
    TetrisApp().run()
