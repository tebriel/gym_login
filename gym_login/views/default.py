"""
Default views
"""
import os
import logging
from datetime import datetime

from googleapiclient.errors import HttpError
from pyramid.view import view_config

from ..sheets import add_login, get_username

DEVELOPMENT = os.getenv('DEVELOPMENT') == 'True'
LOG = logging.getLogger(__name__)


@view_config(route_name='login_user', renderer='json')
def login_user(request):
    """
    Logs a user in using the API
    """
    member_id = request.matchdict.get('id', None)
    errors = {}
    name = 'Unknown'
    success = False
    if member_id is not None:
        now = datetime.now()
        try:
            name = get_username(member_id)
            if name:
                add_login(now, member_id)
                success = True
            else:
                name = 'Lifter'

        except HttpError:
            print("die in a fire")

    return {'gym_name': 'Atlanta Barbell', 'errors': errors, 'success': success,
            'name': name, 'development': DEVELOPMENT, 'member_id': member_id}


@view_config(route_name='gym_login', renderer='../templates/gym_login.jinja2')
def gym_login(request):
    """
    Login view for gym members
    """
    errors = {}
    # We're getting someone trying to log in
    if 'member_id' in request.POST:
        LOG.debug('Got a POST submission')
        member_id = request.params.get('member_id', None)
        if member_id is not None:
            now = datetime.now()
            try:
                add_login(now, member_id)
            except HttpError:
                errors['member_id'] = "Unable to record login, system offline."
                return {'gym_name': 'Atlanta Barbell', 'errors': errors, 'success': False,
                        'development': DEVELOPMENT}

            name = get_username(member_id)
            if not name:
                name = 'Lifter'
            return {'gym_name': 'Atlanta Barbell', 'errors': errors, 'success': True,
                    'name': name, 'development': DEVELOPMENT}

    # Normal page loading/erroring
    return {'gym_name': 'Atlanta Barbell', 'errors': errors, 'success': False,
            'development': DEVELOPMENT}


DB_ERR_MSG = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_gym_login_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
