import flask
from flask import current_app as app
from flask import views


class View(views.MethodView):
    def get(self):
        app.logger.info('TEST %d', 1)
        return flask.jsonify(key='value')
