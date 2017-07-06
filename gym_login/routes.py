"""
List of all routes
"""


def includeme(config):
    """
    All of the routes
    """
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('gym_login', '/')
    config.add_route('login_user', r'/member/{id:\d+}')
    config.add_route('all_members', r'/members')
