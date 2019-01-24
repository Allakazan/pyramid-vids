from pyramid.view import (
    view_config,
    view_defaults
    )


@view_defaults(renderer='../templates/score.pt')
class ScoreViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='score')
    def score(self):
        pipeline = [
            {"$group": {
                "_id": "$genre",
                "sum_up": {"$sum": "$up_votes"},
                "sum_down": {"$sum": "$down_votes"}
            }},
            {"$addFields": {
                "score": {"$subtract": ["$sum_up", {"$divide": ["$sum_down", 2]}]}
            }},
            {"$sort": {"score": -1}}
        ]

        query = list(self.request.db['videos'].aggregate(pipeline))
        data = []

        for line in query:
            data.append({
                "genre": self.request.db['genres'].find_one({"_id": line["_id"]})["name"],
                "score": line["score"]
            })

        return {"data": data}
