import flask
from flask import current_app as app
from flask import views


class View(views.MethodView):
    def get(self):
        ns = app.config.get_namespace('MYMODULE_')
        return flask.jsonify(ns)
