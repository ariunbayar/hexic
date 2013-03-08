from django.shortcuts import render_to_response
from game.utils import memval

def show_board(request):
    board = memval('board')
    users = memval('board_users')
    return render_to_response('admin/show_board.html', {'board': board, 'users': users})

def show_moves(request):
    moves = memval('moves')
    return render_to_response('admin/show_moves.html', {'moves': moves})
