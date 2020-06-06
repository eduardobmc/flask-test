from flask import views


class View(views.MethodView):
    def get(self):
        raise NotImplementedError('oh, oh!')
