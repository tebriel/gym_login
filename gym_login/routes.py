"""
List of all routes
"""


def includeme(config):
    """
    All of the routes
    """
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('gym_login', '/')
    config.add_route('member', r'/member/{id:(\d+|new)}')
