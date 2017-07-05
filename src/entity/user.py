from sqlalchemy import Column, Integer, String, DateTime, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
import datetime
from sqlalchemy.sql import func

Base = declarative_base()
meta = Base.metadata

user_address_link = Table('user_address_link', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('address_id', Integer, ForeignKey('address.id'))
)
question_choice_link = Table('question_choice_link', Base.metadata,
    Column('question_id', Integer, ForeignKey('question.id')),
    Column('choice_id', Integer, ForeignKey('choice.id'))
)



class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    street = Column(String)
    city = Column(String)
    state = Column(String)
    pin = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(150))
    email = Column(String(50), unique=True)
    mobile = Column(String(50), unique=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, email, first_name, last_name, mobile):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.mobile = mobile
    def __repr__(self):
        return 'email: %s' % self.email

class UserHistory(Base):
    __tablename__ = 'user_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    exam_id = Column(Integer, ForeignKey('exam.id'))
#     exam_set_id = Column(Integer, ForeignKey('exam.id'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

class Choice(Base):
    __tablename__ = 'choice'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("question.id"))
    choice_desc = Column(String(150))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    def __init__(self, id, question_id, choiceDesc):
        self.id = id  # primary key
        self.question_id = question_id  # primary key
        self.choiceDesc = choiceDesc


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    ques_desc = Column(String(200))
    ques_topic = Column(String(50))
    single_select = Column(Boolean, unique=False, default=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    def __init__(self, id, quesDesc, singleSelect=True):
        self.id = id  # primary key

        self.quesDesc = quesDesc  # question description
        self.choices = list()  # list of Choice
        self.singleSelect = singleSelect  # Is this a single select or multiple select

class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("question.id"))
    correct_choice_id = Column(Integer, ForeignKey("choice.id"))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    def __init__(self, id, quesId, choices):
        self.id = id  # primary key
        self.quesId = quesId
        self.choices = choices  # list of choiceId


class Exam(Base):
    __tablename__ = 'exam'
    id = Column(Integer, primary_key=True)
    exam_desc = Column(String(50))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    def __init__(self, id, examDesc, examSet):
        self.id = id
        self.examDesc = examDesc  #
        self.examSet = examSet  # list of questions set
