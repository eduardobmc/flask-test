import flask
from flask import views
from werkzeug import exceptions


class View(views.MethodView):
    def get(self):
        return flask.jsonify(method=flask.request.method)

    def post(self):
        payload = flask.request.get_json()
        if payload is None:
            raise exceptions.BadRequest('no post data')
        return flask.jsonify(args=payload)
