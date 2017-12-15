from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,   
    Text,
)
#from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from .meta import Base


class Post(Base):
    """ The SQLAlchemy declarative model class for a Page object. """
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    data = Column(Text, nullable=False) 

    creator_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User',backref= 'users')