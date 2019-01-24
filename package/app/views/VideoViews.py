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
            vid = {
                "name": video['name'],
                "genre": self.request.db['genres'].find_one({"_id": video['genre']})["name"],
                "code": video['code'],
                "up_votes": video['up_votes'],
                "down_votes": video['down_votes']
            }

            return {'video': vid}

    @view_config(route_name='thumbs', renderer='json')
    def thumbs(self):
        thumb = self.request.params.get('thumb', None)
        code = self.request.params.get('code', None)
        video = self.request.db['videos'].find_one({"code": code})
        post = {}
        if video is not None and (thumb == 'up' or thumb == 'down'):
            if thumb == 'up':
                post['up_votes'] = video['up_votes'] + 1
                self.request.db['videos'].update_one({'code': code}, {"$set": post}, upsert=False)
            elif thumb == 'down':
                post['down_votes'] = video['down_votes'] + 1
                self.request.db['videos'].update_one({'code': code}, {"$set": post}, upsert=False)
            return {"status": "ok", "thumb": thumb}
        else:
            return {"status": "error"}

    @view_config(route_name='not-found', renderer='../templates/404.pt')
    def not_found(self):
        return {}
