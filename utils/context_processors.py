def inject_globals(request):
    """ Inject account_id for base template """
    ctx = {'account_id': request.session.get('account_id')}
    return ctx
