from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from user import User, Base
from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()
if __name__ == '__main__':
    engine = create_engine('sqlite:///exam.db', echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    ed_user = User('ed', 'Ed Jones', 'edspassword',None)
    session.add(ed_user)
    session.commit()
