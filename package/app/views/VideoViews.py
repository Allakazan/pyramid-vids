from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    view_config,
    view_defaults
    )


@view_defaults(renderer='../templates/video.pt')
class TutorialViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='video')
    def video(self):
        code = self.request.params.get('v', 1)
        video = self.request.db['videos'].find_one({"code": code})

        if video is None:
            url = self.request.route_url('not-found')
            return HTTPFound(location=url)
        else:
            return {'name': 'VIDEO'}

    @view_config(route_name='not-found', renderer='../templates/404.pt')
    def not_found(self):
        return {}
