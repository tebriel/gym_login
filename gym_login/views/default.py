"""
Default views
"""
import logging

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MemberModel, LoginRecordModel

LOG = logging.getLogger(__name__)


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
        try:
            query = request.dbsession.query(MemberModel)
            one = query.filter(MemberModel.member_id == member_id).\
                filter_by(active=True).first()
            if one is None:
                errors = {'member_id': 'Member ID Not Found'}
                LOG.error('Member ID Not Found: %s', member_id)
            else:
                record = LoginRecordModel(member_id=one.id)
                request.dbsession.add(record)
        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)

        if len(errors) == 0:
            return {'data': request.params['member_id'], 'name': one.name, 'success': True}

    # Normal page loading/erroring
    return {'gym_name': 'Atlanta Barbell', 'errors': errors, 'success': False}


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
