from decorators import render_to


@render_to('public/index.html')
def index(request):
    return {}
