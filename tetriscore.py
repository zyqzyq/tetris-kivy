# -*- coding: utf-8 -*-
#from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.event import EventDispatcher


#class SparseGridLayout(FloatLayout):
class SparseGridLayout(RelativeLayout):

    rows = NumericProperty(1)
    columns = NumericProperty(1)
    shape = ReferenceListProperty(rows, columns)

    def do_layout(self, *args):
        # calculate shape of grid cells
        shape_hint = (1. / self.columns, 1. / self.rows)
        for child in self.children:
            # make each child of grid the size of a cell
            child.size_hint = shape_hint

            # set positioning of child to align to grid
            if not hasattr(child, 'row'):
                child.row = 0
            if not hasattr(child, 'column'):
                child.column = 0
            child.pos_hint = {'x': shape_hint[0] * child.column,
                              'y': shape_hint[1] * child.row}
        super(SparseGridLayout, self).do_layout(*args)


class GridEntry(EventDispatcher):

    row = NumericProperty(0)
    column = NumericProperty(0)
    grid_pos = ReferenceListProperty(row, column)