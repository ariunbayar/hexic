def inject_globals(request):
    """ Inject admin_id for base template """
    ctx = {'session_admin_id': request.session.get('admin_id')}
    return ctx
