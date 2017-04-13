# -*- coding: utf-8 -*-

from kivy.properties import ObjectProperty, StringProperty, \
    OptionProperty, ReferenceListProperty, ListProperty
from kivy.uix.relativelayout import RelativeLayout
#from kivy.uix.button import Button
from kivy.uix.image import Image

from tetriscore import GridEntry


class Piece(RelativeLayout, GridEntry):

    name = StringProperty('L')
    mode = OptionProperty('up', options=['up', 'dn', 'lt', 'rt'])
    brick_a = ObjectProperty(None)
    brick_b = ObjectProperty(None)
    brick_c = ObjectProperty(None)
    brick_0 = ObjectProperty(None)
    bricks = ReferenceListProperty(brick_a, brick_b, brick_c, brick_0)
    color = ListProperty([1, 1, 1, 1])

    def on_grid_pos(self, *args, **kwargs):
        self.pos_hint = {'x': self.size_hint[0] * self.column,
                         'y': self.size_hint[1] * self.row}

    def fall(self, *args):
        self.row = self.row - 1

    def strifel(self):
        self.column = self.column - 1

    def strifer(self):
        self.column = self.column + 1

    def shift_left(self):
        if self.mode is 'up':
            self.mode = 'lt'
        elif self.mode is 'dn':
            self.mode = 'rt'
        elif self.mode is 'rt':
            self.mode = 'up'
        elif self.mode is 'lt':
            self.mode = 'dn'

    def shift_right(self):
        if self.mode is 'up':
            self.mode = 'rt'
        elif self.mode is 'dn':
            self.mode = 'lt'
        elif self.mode is 'rt':
            self.mode = 'dn'
        elif self.mode is 'lt':
            self.mode = 'up'

    def release_bricks(self):
        for brick in self.bricks:
            self.remove_widget(brick)

    def factory(name):
        if name is 'L':
            return LPiece()
        if name is 'J':
            return JPiece()
        if name is 'S':
            return SPiece()
        if name is 'O':
            return OPiece()
        if name is 'T':
            return TPiece()
        if name is 'I':
            return IPiece()
        if name is 'Z':
            return ZPiece()
    factory = staticmethod(factory)


class LPiece(Piece):

    def shift_right(self):
        if self.mode in ['up', 'dn']:
            self.brick_a.pos_hint = {'x': 0, 'y': 1}
            self.brick_b.pos_hint = {'x': 0, 'y': -1}
            brick_c_pos = self.brick_c.pos_hint
            self.brick_c.pos_hint = {'x': brick_c_pos['x'],
                'y': brick_c_pos['y'] * -1}
        else:
            self.brick_a.pos_hint = {'x': -1, 'y': 0}
            self.brick_b.pos_hint = {'x': 1, 'y': 0}
            brick_c_pos = self.brick_c.pos_hint
            self.brick_c.pos_hint = {'y': brick_c_pos['y'],
                'x': brick_c_pos['x'] * -1}
        super(LPiece, self).shift_right()

    def shift_left(self):
        if self.mode in ['up', 'dn']:
            self.brick_a.pos_hint = {'x': 0, 'y': 1}
            self.brick_b.pos_hint = {'x': 0, 'y': -1}
            brick_c_pos = self.brick_c.pos_hint
            self.brick_c.pos_hint = {'y': brick_c_pos['y'],
                'x': brick_c_pos['x'] * -1}
        else:
            self.brick_a.pos_hint = {'x': -1, 'y': 0}
            self.brick_b.pos_hint = {'x': 1, 'y': 0}
            brick_c_pos = self.brick_c.pos_hint
            self.brick_c.pos_hint = {'x': brick_c_pos['x'],
                'y': brick_c_pos['y'] * -1}
        super(LPiece, self).shift_left()


class TPiece(Piece):

    def shift_right(self):
        if self.mode in ['up', 'dn']:
            self.brick_a.pos_hint = {'x': 0, 'y': 1}
            self.brick_b.pos_hint = {'x': 0, 'y': -1}
            if self.mode is 'up':
                brick_c_pos = self.brick_c.pos_hint
                self.brick_c.pos_hint = {'x': brick_c_pos['x'] - 1,
                    'y': brick_c_pos['y'] + 1}
            else:
                brick_c_pos = self.brick_c.pos_hint
                self.brick_c.pos_hint = {'x': brick_c_pos['x'] + 1,
                    'y': brick_c_pos['y'] - 1}
        else:
            self.brick_a.pos_hint = {'x': -1, 'y': 0}
            self.brick_b.pos_hint = {'x': 1, 'y': 0}
            if self.mode is 'rt':
                brick_c_pos = self.brick_c.pos_hint
                self.brick_c.pos_hint = {'x': brick_c_pos['x'] + 1,
                    'y': brick_c_pos['y'] + 1}
            else:
                brick_c_pos = self.brick_c.pos_hint
                self.brick_c.pos_hint = {'x': brick_c_pos['x'] - 1,
                    'y': brick_c_pos['y'] - 1}
        super(TPiece, self).shift_right()

    def shift_left(self):
        if self.mode in ['up', 'dn']:
            self.brick_a.pos_hint = {'x': 0, 'y': 1}
            self.brick_b.pos_hint = {'x': 0, 'y': -1}
            if self.mode is 'up':
                brick_c_pos = self.brick_c.pos_hint
                self.brick_c.pos_hint = {'x': brick_c_pos['x'] + 1,
                    'y': brick_c_pos['y'] + 1}
            else:
                brick_c_pos = self.brick_c.pos_hint
                self.brick_c.pos_hint = {'x': brick_c_pos['x'] - 1,
                    'y': brick_c_pos['y'] - 1}
        else:
            self.brick_a.pos_hint = {'x': -1, 'y': 0}
            self.brick_b.pos_hint = {'x': 1, 'y': 0}
            if self.mode is 'rt':
                brick_c_pos = self.brick_c.pos_hint
                self.brick_c.pos_hint = {'x': brick_c_pos['x'] + 1,
                    'y': brick_c_pos['y'] - 1}
            else:
                brick_c_pos = self.brick_c.pos_hint
                self.brick_c.pos_hint = {'x': brick_c_pos['x'] - 1,
                    'y': brick_c_pos['y'] + 1}
        super(TPiece, self).shift_left()


class JPiece(Piece):

    def shift_left(self):
        if self.mode in ['up', 'dn']:
            self.brick_a.pos_hint = {'x': 0, 'y': 1}
            self.brick_b.pos_hint = {'x': 0, 'y': -1}
            brick_c_pos = self.brick_c.pos_hint
            self.brick_c.pos_hint = {'x': brick_c_pos['x'],
                'y': brick_c_pos['y'] * -1}
        else:
            self.brick_a.pos_hint = {'x': -1, 'y': 0}
            self.brick_b.pos_hint = {'x': 1, 'y': 0}
            brick_c_pos = self.brick_c.pos_hint
            self.brick_c.pos_hint = {'y': brick_c_pos['y'],
                'x': brick_c_pos['x'] * -1}
        super(JPiece, self).shift_left()

    def shift_right(self):
        if self.mode in ['up', 'dn']:
            self.brick_a.pos_hint = {'x': 0, 'y': 1}
            self.brick_b.pos_hint = {'x': 0, 'y': -1}
            brick_c_pos = self.brick_c.pos_hint
            self.brick_c.pos_hint = {'y': brick_c_pos['y'],
                'x': brick_c_pos['x'] * -1}
        else:
            self.brick_a.pos_hint = {'x': -1, 'y': 0}
            self.brick_b.pos_hint = {'x': 1, 'y': 0}
            brick_c_pos = self.brick_c.pos_hint
            self.brick_c.pos_hint = {'x': brick_c_pos['x'],
                'y': brick_c_pos['y'] * -1}
        super(JPiece, self).shift_right()


class SPiece(Piece):

    def shift_right(self):
        if self.mode in ['up', 'dn']:
            self.brick_a.pos_hint = {'x': -1, 'y': 0}
        else:
            self.brick_a.pos_hint = {'x': 1, 'y': 0}
        brick_c_pos = self.brick_c.pos_hint
        self.brick_c.pos_hint = {'y': brick_c_pos['y'] * -1,
            'x': brick_c_pos['x']}
        super(SPiece, self).shift_right()

    def shift_left(self):
        if self.mode in ['up', 'dn']:
            self.brick_a.pos_hint = {'x': -1, 'y': 0}
        else:
            self.brick_a.pos_hint = {'x': 1, 'y': 0}
        brick_c_pos = self.brick_c.pos_hint
        self.brick_c.pos_hint = {'y': brick_c_pos['y'] * -1,
            'x': brick_c_pos['x']}
        super(SPiece, self).shift_left()


class ZPiece(Piece):

    def shift_right(self):
        if self.mode in ['up', 'dn']:
            self.brick_b.pos_hint = {'x': 0, 'y': 1}
        else:
            self.brick_b.pos_hint = {'x': 0, 'y': -1}
        brick_c_pos = self.brick_c.pos_hint
        self.brick_c.pos_hint = {'y': brick_c_pos['y'],
            'x': brick_c_pos['x'] * -1}
        super(ZPiece, self).shift_right()

    def shift_left(self):
        self.shift_right()


class IPiece(Piece):

    def shift_right(self):
        if self.mode in ['up', 'dn']:
            self.brick_a.pos_hint = {'x': 0, 'y': -1}
            self.brick_b.pos_hint = {'x': 0, 'y': 1}
            self.brick_c.pos_hint = {'x': 0, 'y': 2}
        else:
            self.brick_a.pos_hint = {'x': -1, 'y': 0}
            self.brick_b.pos_hint = {'x': 1, 'y': 0}
            self.brick_c.pos_hint = {'x': 2, 'y': 0}
        super(IPiece, self).shift_right()

    def shift_left(self):
        self.shift_right()


class OPiece(Piece):
    pass


class Brick(Image, GridEntry):
    pass