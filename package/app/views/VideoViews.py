import random, string, os, shutil
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

    @view_config(route_name='upload', renderer='../templates/upload.pt')
    def upload(self):
        post = self.request.POST
        genres = list(self.request.db['genres'].find())
        errors = []
        show_msg = False
        if len(list(post)) > 0:
            show_msg = True

            name = post["name"]
            genre = post["genre"]
            thumbfile = post["thumbnail"]
            videofile = post["video"]

            if not name:
                errors.append("Name field cannot be empty")
            if thumbfile == b'':
                errors.append("Thumbnail field cannot be empty")
            else:
                if not (thumbfile.filename.endswith('.png') or thumbfile.filename.endswith('.gif') or
                        thumbfile.filename.endswith('.jpeg') or thumbfile.filename.endswith('.jpg') or
                        thumbfile.filename.endswith('.png')):
                    errors.append("Wrong thumbnail extension")
            if videofile == b'':
                errors.append("Video field cannot be empty")
            else:
                if not videofile.filename.endswith('.mp4'):
                    errors.append("Wrong video extension, application only accept .mp4")

            if len(errors) == 0:
                new_code = self.get_random_code()
                path = '../data/' + new_code

                if not os.path.exists(path):
                    os.chdir(os.path.dirname(os.path.realpath(__file__)))
                    os.mkdir(path)

                    self.save_files(thumbfile, path, "thumb")
                    self.save_files(videofile, path, "video")

                    list_ids = list(self.request.db['videos'].find().sort([("_id", -1)]).limit(1))
                    if len(list_ids) > 0:
                        last_id = list_ids[0]["_id"]
                    else:
                        last_id = 1

                    post = {
                        "_id": last_id + 1,
                        "name": name,
                        "genre": int(genre),
                        "code": new_code,
                        "up_votes": 0,
                        "down_votes": 0
                    }

                    inserted_id = self.request.db['videos'].insert_one(post).inserted_id

        return {"genres": genres, "show_msg": show_msg, "errors": errors}

    def save_files(self, file, path, name):
        thumb_ext = os.path.splitext(file.filename)[1]

        input_file = file.file
        file_path = os.path.join(path, name + thumb_ext)
        temp_file_path = file_path + '~'

        input_file.seek(0)
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        os.rename(temp_file_path, file_path)

    def get_random_code(self):
        code = ''.join(random.SystemRandom().choices(string.ascii_uppercase + string.ascii_lowercase, k=12))
        video = self.request.db['videos'].find_one({"code": code})

        if video is not None:
            return self.get_random_code()
        else:
            return code

    @view_config(route_name='not-found', renderer='../templates/404.pt')
    @view_config(context='pyramid.httpexceptions.HTTPNotFound', renderer='../templates/404.pt')
    def not_found(self):
        self.request.response.status_int = 404
        return {}
