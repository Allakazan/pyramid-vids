import math
from pyramid.view import (
    view_config,
    view_defaults
    )


@view_defaults(renderer='../templates/home.pt')
class HomeViews:
    def __init__(self, request):
        self.request = request
        self.limit = 8

    @view_config(route_name='home')
    def home(self):

        count = self.request.db['videos'].count_documents({})
        pages = math.ceil(count/self.limit)

        active_page = int(self.request.params.get('page', 1))

        if active_page < 1:
            active_page = 1

        if active_page > pages:
            active_page = pages

        skip = self.limit * (active_page-1)

        videos = []
        for vid in self.request.db['videos'].find().sort([("_id", -1)]).limit(self.limit).skip(skip):
            videos.append({
                "name": vid['name'],
                "genre": self.request.db['genres'].find_one({"_id": vid['genre']})["name"],
                "code": vid['code'],
                "up_votes": vid['up_votes'],
                "down_votes": vid['down_votes']
            })
        return {'videos': videos, 'pages': pages, 'active_page': active_page, 'count': pages}
