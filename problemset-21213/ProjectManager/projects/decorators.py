from functools import wraps


# noinspection PyPep8Naming
class projects_panel(object):
    def __init__(self, permissions=None):
        self.permissions = permissions

    def __call__(self, view_func):

        @wraps(view_func)
        def _wrapper_view(request, *args, **kwargs):

            

            return view_func(request, *args, **kwargs)

        return _wrapper_view
