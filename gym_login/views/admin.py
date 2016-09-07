"""
Default views
"""
import logging

from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from sqlalchemy import desc

from ..models import MemberModel, LoginRecordModel

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


@view_config(route_name='member', renderer='../templates/member.jinja2')
def add_member(request):
    """
    Create new member record
    """
    cur_member = None
    errors = {}
    url_id = request.matchdict.get('id')
    member = MemberModel(fname='', lname='', member_id='', active=True)

    if url_id is not None:
        # Looks like we're trying to view/edit/deactivate, let's see if that exists
        cur_member = request.dbsession.query(MemberModel).\
            filter(MemberModel.id == url_id).first()
        if cur_member is not None:
            member = cur_member

    if request.method == 'POST':
        LOG.debug('Creating new member: %s', request.POST)
        # Set up the user from the POST
        member.fname = request.POST.get('fname', '')
        member.lname = request.POST.get('lname', '')
        member.member_id = request.POST.get('member_id')
        member.active = request.POST.get('active') == 'on'

        # TODO: Validate that it's all digits
        if len(request.POST.get('member_id', '')) != 4:
            errors['member_id'] = "Member ID must be 4 digits"
        elif not member.id and member_exists(request.dbsession, request.POST.get('member_id')):
            errors['member_id'] = "Member ID taken, choose another"
        elif member.id is None:
            # if this is a new member
            request.dbsession.add(member)
            member = MemberModel(fname='', lname='', member_id='', active=True)
            errors['status'] = "Successfully created user."
        else:
            errors['status'] = "Successfully updated user."

    elif request.method == 'DELETE':
        if member.id is not None:
            LOG.debug("Deactivating user: %s", member.id)
            member.active = False

    return {'errors': errors, 'member': member}


@view_config(route_name='all_members', renderer='../templates/member_list.jinja2')
def all_members(request):
    """
    View All Members
    """
    members_query = request.dbsession.query(MemberModel)
    sorter = request.params.get('sort', 'lname')
    order = request.params.get('order', 'asc')
    if sorter == 'last_signin':
        members_query = members_query.join(MemberModel.logins)
        if order == 'desc':
            members_query = members_query.order_by(desc(LoginRecordModel.date))
        else:
            members_query = members_query.order_by(LoginRecordModel.date)
    else:
        if order == 'desc':
            members_query = members_query.order_by(desc("LOWER({0})".format(sorter)))
        else:
            members_query = members_query.order_by("LOWER({0})".format(sorter))

    members = members_query.all()

    return {'members': members, 'sorter': sorter, 'order': order, 'page_name': 'members'}
