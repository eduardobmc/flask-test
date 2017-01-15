import flask
from flask import views


class View(views.MethodView):
    def get(self):
        code = flask.request.args['code']
        return flask.jsonify(key=code)
