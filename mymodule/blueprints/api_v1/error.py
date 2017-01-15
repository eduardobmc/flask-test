from flask import views


class View(views.MethodView):
    def get(self):
        raise Exception('oh, oh!')
