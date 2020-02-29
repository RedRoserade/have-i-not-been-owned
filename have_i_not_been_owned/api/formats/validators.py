from bson import ObjectId
from bson.errors import InvalidId
from jsonschema import draft4_format_checker

# See https://connexion.readthedocs.io/en/latest/cookbook.html#custom-type-format


@draft4_format_checker.checks('objectid')
def is_objectid(val):
    """
    Validator for `objectid`-formatted strings in the OpenAPI spec.
    :param val:
    :return:
    """
    if isinstance(val, ObjectId):
        return True

    try:
        ObjectId(val)
        return True
    except InvalidId:
        return False
