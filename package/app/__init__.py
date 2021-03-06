from pyramid.config import Configurator
try:
    # for python 2
    from urlparse import urlparse
except ImportError:
    # for python 3
    from urllib.parse import urlparse

from gridfs import GridFS
from pymongo import MongoClient


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    config.add_route('home', '/')
    config.add_route('video', '/watch')
    config.add_route('thumbs', '/thumbs')
    config.add_route('upload', '/upload')
    config.add_route('score', '/score')
    config.add_route('not-found', '/404')

    config.add_static_view(name='public', path='app:public')
    config.add_static_view(name='data', path='app:data')

    db_url = urlparse(settings['mongo_uri'])
    config.registry.db = MongoClient(
        host=db_url.hostname,
        port=db_url.port,
    )

    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db

    # def add_fs(request):
    #    return GridFS(request.db)

    config.add_request_method(add_db, 'db', reify=True)
    # config.add_request_method(add_fs, 'fs', reify=True)

    config.scan('.views')
    return config.make_wsgi_app()
