"""
Handle Forbidden Errors
"""
from pyramid.view import forbidden_view_config


@forbidden_view_config(renderer='../templates/404.jinja2')
def forbidden_view(request):
    """
    Forbidden View Config
    """
    request.response.status = 403
    return {}
