from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

database_path = '/tmp'
if not os.path.exists(database_path):
    os.makedirs(database_path)
engine = create_engine('sqlite:///' + os.path.join(database_path, 'tap.db') +'?check_same_thread=False', convert_unicode=True)
db_session = scoped_session(sessionmaker(autoflush=False,bind=engine))
# db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models.models
    Base.metadata.create_all(bind=engine)

def clear_db():
    from models.models import TapRecord
    TapRecord.__table__.drop(engine)