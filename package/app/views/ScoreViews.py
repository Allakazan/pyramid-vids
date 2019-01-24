from pyramid.view import (
    view_config,
    view_defaults
    )


@view_defaults(renderer='../templates/home.pt')
class ScoreViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='score')
    def score(self):
        print("ss")
