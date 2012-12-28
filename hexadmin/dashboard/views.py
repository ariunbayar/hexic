from django.shortcuts import render_to_response
from django.template import RequestContext

from board.models import Board


def index(request):
    boards = Board.objects.all().order_by('board', 'position')
    boards = Board.objects.values_list('name', flat=True).distinct('name')
    board_group = [[(y * 10 + x, y, x) for x in range(10)] for y in range(10)]

    ctx = {'boards': boards, 'board_group': board_group}
    return render_to_response('dashboard/index.html',
                              RequestContext(request, ctx))
