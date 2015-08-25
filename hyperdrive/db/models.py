from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship,backref
from sqlalchemy.sql import text

Model = declarative_base()

class BaseModel(Model):
    __abstract__ = True
    __table_args__ = {
	'mysql_engine': 'InnoDB',
	'mysql_charset': 'utf8'
    }
    def save(self,session):
	session.add(self)	
	session.flush()

    def update(self,values):
	for k,v in values.iteritems():
	    setattr(self,k,v)

class Item(BaseModel):
    __tablename__ = 'items'
   
    id = Column(String(32),primary_key=True)
    name = Column(String(50))
    img = Column(String(600),default='')
    price = Column(Integer)
    size = Column(Integer)
    origin = Column(String(100), default='')
    created = Column(DateTime, default=func.now())
 
