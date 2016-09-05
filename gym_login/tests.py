"""
Test loading views
"""
import unittest
import transaction

from pyramid import testing


def dummy_route_url(url):
    """
    Fake route_url method
    """
    return url


def dummy_request(dbsession):
    """
    Creates a dummy request with a database session
    """
    dummy = testing.DummyRequest(dbsession=dbsession)
    dummy.route_url = dummy_route_url
    return dummy


class BaseTest(unittest.TestCase):
    """
    Base Test Class
    """
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        """
        Initialzes the test database
        """
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        """
        Clean up after ourselves
        """
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestGymLogin(BaseTest):
    """
    Test how we handle logins
    """
    def setUp(self):
        super(TestGymLogin, self).setUp()
        self.init_database()

        from .models import MemberModel

        model = MemberModel(fname='Test', member_id='3333', active=True)
        inactive = MemberModel(fname='Inactive', member_id='0000', active=False)
        self.session.add_all([model, inactive])

    def test_get_gym_login(self):
        """
        Test getting the base data
        """
        from .views.default import gym_login
        info = gym_login(dummy_request(self.session))
        assert info['gym_name'] == 'Atlanta Barbell'
        assert info['errors'] == {}

    def test_post_gym_login(self):
        """
        Test submitting the gym login info
        """
        from .views.default import gym_login
        request = dummy_request(self.session)
        request.params['member_id'] = '3333'
        info = gym_login(request)
        assert info['name'] == 'Test'

    def test_post_gym_login_unauth(self):
        """
        Test submitting the gym login info
        """
        from .views.default import gym_login
        request = dummy_request(self.session)
        request.params['member_id'] = '9999'
        info = gym_login(request)
        assert info['errors']['member_id'] is not None

    def test_post_gym_login_inactive(self):
        """
        Test submitting the gym login info
        """
        from .views.default import gym_login
        request = dummy_request(self.session)
        request.params['member_id'] = '0000'
        info = gym_login(request)
        assert info['errors']['member_id'] is not None


class TestGymAdmin(BaseTest):
    """
    Test how we handle logins
    """
    def setUp(self):
        super(TestGymAdmin, self).setUp()
        self.init_database()

        from .models import MemberModel

        self.model = MemberModel(fname='Test', member_id='3333', active=True)
        self.inactive = MemberModel(fname='Inactive', member_id='0000', active=False)
        self.session.add_all([self.model, self.inactive])

    def test_get_add_member(self):
        """
        Test getting the add member page
        """
        from .views.admin import add_member
        info = add_member(dummy_request(self.session))
        assert info['errors'] == {}

    def test_add_member(self):
        """
        Test adding a new member to the database
        """
        from .views.admin import add_member
        request = dummy_request(self.session)
        request.method = 'POST'
        request.POST['member_id'] = '1111'
        request.POST['fname'] = 'Test'
        request.POST['lname'] = 'User'
        info = add_member(request)
        assert info['errors']['status'] is not None

    def test_add_member_dup_id(self):
        """
        Test adding a new member to the database when the user id already exists
        """
        from .views.admin import add_member
        request = dummy_request(self.session)
        request.method = 'POST'
        request.POST['member_id'] = '3333'
        request.POST['fname'] = 'Test'
        request.POST['lname'] = 'User'
        info = add_member(request)
        assert len(info['errors']) == 1
        assert info['member'].fname == 'Test'
        assert info['member'].lname == 'User'
        assert info['member'].member_id == '3333'

    def test_update_member(self):
        """
        Test adding a new member to the database
        """
        from .views.admin import add_member
        from .models import MemberModel

        cur_id = self.session.query(MemberModel).\
            filter(MemberModel.member_id == '3333').first().id
        request = dummy_request(self.session)
        request.method = 'POST'
        request.matchdict['id'] = cur_id
        request.POST['member_id'] = '3333'
        request.POST['fname'] = 'Test'
        request.POST['lname'] = 'User'
        request.POST['active'] = 'false'
        info = add_member(request)
        assert len(info['errors']) == 0
        model = self.session.query(MemberModel).\
            filter(MemberModel.id == cur_id).first()
        assert model.active is False
