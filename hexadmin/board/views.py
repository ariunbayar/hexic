from django.contrib.messages import add_message as flash, SUCCESS, WARNING
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect as Redirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson as json
from django.views.decorators.http import require_POST

from board.forms import BoardForm
from board.models import Board, new_cell


def board_new(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board_cell = new_cell()
            board_row = [board_cell for i in range(10)]
            board_content = [board_row for i in range(10)]
            content = json.dumps(board_content)
            board_name = form.cleaned_data['board_name']
            for pos in range(100):
                Board.objects.create(name=board_name, board=content,
                                     position=pos)
            flash(request, SUCCESS, 'New board %s is created!' % board_name)
            return Redirect(reverse('board-show', args=(board_name, 0)))
    else:
        form = BoardForm()
    ctx = {'form': form}
    return render_to_response('board/board_new.html',
                              RequestContext(request, ctx))


def board_show(request, name, position):
    board = get_object_or_404(Board, name=name, position=position)
    board_group = [[(y * 10 + x, y, x) for x in range(10)] for y in range(10)]
    board_group[board.y][board.x] = None

    ctx = {'board': board, 'board_group': board_group,
           'board_left': Board.get_board_left(board),
           'board_right': Board.get_board_right(board),
           'board_up': Board.get_board_up(board),
           'board_down': Board.get_board_down(board)}
    return render_to_response('board/board_show.html',
                              RequestContext(request, ctx))


@require_POST
def board_save(request, name, position):
    board = get_object_or_404(Board, name=name, position=position)
    try:
        board_data = request.POST.get('data')
        import logging
        logging.error(board_data)
        rows = []
        for row_data in board_data.split(';'):
            row = []
            for cell_data in row_data.split(','):
                cell = {'type': 'off'}
                if cell_data:
                    count, player = cell_data.split('-')
                    cell.update({'type': 'on', 'count': int(count),
                                 'player': int(player)})
                row.append(cell)
            rows.append(row)
        board.board = json.dumps(rows)
    except:
        flash(request, WARNING, 'Failed to save the board!')
    else:
        board.save()
        flash(request, SUCCESS, 'Board successfully saved!')

    return Redirect(reverse('board-show', args=(name, position)))
