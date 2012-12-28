import math

from django.db import models
from django.utils import simplejson as json


def new_cell(type='on', count=0, player=0):
    cell = dict(type=type, count=count, player=player)
    return cell


class Board(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    board = models.TextField()
    position = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'hex_board'
        unique_together = ('name', 'position')

    @property
    def x(self):
        return self.position % 10

    @property
    def y(self):
        return int(math.floor(self.position / 10))

    def get_cells(self):
        return json.loads(self.board)

    @classmethod
    def get_board_right(cls, board):
        """ Returns None if there is none or doesn't exist """
        if board.x < 9:
            return cls.objects.get(name=board.name,
                                   position=(board.position + 1))
        return None

    @classmethod
    def get_board_left(cls, board):
        """ Returns None if there is none or doesn't exist """
        if board.x > 0:
            return cls.objects.get(name=board.name,
                                   position=(board.position - 1))
        return None

    @classmethod
    def get_board_down(cls, board):
        """ Returns None if there is none or doesn't exist """
        if board.y < 9:
            return cls.objects.get(name=board.name,
                                   position=(board.position + 10))
        return None

    @classmethod
    def get_board_up(cls, board):
        """ Returns None if there is none or doesn't exist """
        if board.y > 0:
            return cls.objects.get(name=board.name,
                                   position=(board.position - 10))
        return None
