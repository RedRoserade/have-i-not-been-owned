from bson import ObjectId
from connexion.apps.flask_app import FlaskJSONEncoder


class CustomJSONEncoder(FlaskJSONEncoder):

    def default(self, o):
        # Handle ObjectIDs without us having to manually `str`-ing them.
        if isinstance(o, ObjectId):
            return str(o)

        return super().default(o)
