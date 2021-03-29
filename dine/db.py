#coding : utf-8
import os
import datetime
from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("{}://{}:{}@{}:{}/{}"\
    			.format(os.environ["DBMS"], os.environ["USER_NAME"], os.environ["PASSWORD"], \
                os.environ["HOST"], os.environ["DBMS_PORT"], os.environ["DATABASE"]), encoding="utf8", echo=True)

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    line_id = Column(String, primary_key=True)
    discord_id = Column(String)

class Password(Base):
    __tablename__ = "password"
    line_id = Column(String, primary_key=True)
    password = Column(Integer, unique=True)
    register_time = Column(DateTime)

class DiscordServer(Base):
	__tablename__ = "dicord_server"
	server_id = Column(String, primary_key=True)
	channel_id = Column(String)

class ServerInfo(Base):
    __tablename__ = "server_info"
    server_id = Column(String, primary_key=True)
    line_id = Column(String)
    auth_flag = Column(Boolean, default=False)
    text_notice = Column(Boolean, default=True)
    voice_notice = Column(Boolean, default=True)

class LineCrud:
    def add_following_to_password(self, session, line_id, password):
        session.add(Password(line_id=line_id, password=password, register_time=datetime.datetime.now()))
    
    def exists_password(self, session, password):
        return session.query(session.query(Password).filter(Password.password == password).exists()).scalar()

    def exists_line_user(self, session, line_id):
        return session.query(session.query(Password).filter(Password.line_id == line_id).exists()).scalar()

class ScheduleManager():
    def time_over_user(self, session):
        nowtime = datetime.datetime.now()
        session.query(Password).filter(Password.register_time < nowtime - datetime.timedelta(minutes=5)).delete()

class SessionManager:
    @contextmanager
    def session_create(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
            engine.dispose()

def create_db():
    Base.metadata.create_all(engine)
    engine.dispose()