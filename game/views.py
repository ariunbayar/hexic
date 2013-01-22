from decorators import render_to, check_login


@check_login
@render_to('game/animation.html')
def board(request):
    return {}
