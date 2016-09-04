"""
Base Model Class
"""

# pylint: disable=R0903,C0103


from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    sql,
    orm,
)

from sqlalchemy.ext.hybrid import hybrid_property

from .meta import Base


class MemberModel(Base):
    """
    Storage of a member's data
    TODO: Couldn't figure out unique constraint where member_id unique but only when active=True,
      we only want the constraint to be on members that are active, because having previous
      members who had the same id shouldn't matter.
    """
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    fname = Column(Text)
    lname = Column(Text)
    # All member id's are 4 characters long...we hope
    member_id = Column(String(4), nullable=False)
    active = Column(Boolean(create_constraint=False))
    logins = orm.relationship('LoginRecordModel', back_populates='member')

    @hybrid_property
    def name(self):
        """
        Returns the full name of a member
        """
        fname = self.fname or ""
        lname = self.lname or ""
        result = "{fname} {lname}".format_map({'fname': fname, 'lname': lname})
        return result.strip()


class LoginRecordModel(Base):
    """
    Records a login event by a member
    """
    __tablename__ = 'logins'
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('members.id'))
    date = Column(DateTime, default=sql.func.now())
    member = orm.relationship('MemberModel', back_populates='logins')
