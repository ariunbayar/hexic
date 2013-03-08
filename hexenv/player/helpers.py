from player.models import Player


def get_design_by_player(user_id):
    player = Player.objects.get(pk=user_id)
    return player.design if player else 0


def get_player(session):
    player = Player.objects.get(pk=session['id'])
    return player
