import flask

from . import upload
from . import test
from . import error
from . import keys
from . import config
from . import crud


blueprint = flask.Blueprint('v1', __name__, url_prefix='/api/v1')

blueprint.add_url_rule('/upload', view_func=upload.post, methods=['POST'])
blueprint.add_url_rule('/upload2', view_func=upload.post2, methods=['POST'])

for rule, pkg in [
    ('/test', test),
    ('/error', error),
    ('/keys', keys),
    ('/config', config),
    ('/crud', crud),
]:
    cls = pkg.View
    view_func = cls.as_view(pkg.__name__)
    blueprint.add_url_rule(rule, view_func=view_func, methods=cls.methods)
