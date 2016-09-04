"""
Default views
"""
import logging

from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MemberModel

LOG = logging.getLogger(__name__)


def member_exists(session, member_id):
    """
    Determine if an active member exists with a member_id
    """
    try:
        query = session.query(MemberModel)
        one = query.filter(MemberModel.member_id == member_id).\
            filter_by(active=True).first()
        if one is None:
            LOG.debug("Active Member with ID: %s not found.", member_id)
            return False
        else:
            LOG.debug("Active Member with ID: %s found.", member_id)
            return True
    except DBAPIError:
        LOG.exception("Could not determine users existence for id: %s", member_id)
        return True


@view_config(route_name='add_member', renderer='../templates/add_member.jinja2')
def add_member(request):
    """
    Create new member record
    """
    errors = {}
    if request.method == 'POST':
        LOG.debug('Creating new member: %s', request.POST)
        # TODO: Validate that it's all digits
        if len(request.POST.get('member_id', '')) != 4:
            errors['member_id'] = "Member ID must be 4 digits"
        elif member_exists(request.dbsession, request.POST.get('member_id')):
            errors['member_id'] = "Member ID taken, choose another"
        else:
            new_member = MemberModel(fname=request.POST.get('fname', ''),
                                     lname=request.POST.get('lname', ''),
                                     member_id=request.POST.get('member_id'),
                                     active=True)
            request.dbsession.add(new_member)
            errors['status'] = "Successfully created user."

    return {'errors': errors}
