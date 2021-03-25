#coding : utf-8
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Users(Base):
    __tablename__ = "users"
    line_id = Column(String, primary_key=True)
    discord_id = Column(String)

class Password(Base):
    __tablename__ = "password"
    line_id = Column(String, primary_key=True)
    password = Column(Integer, unique=True)

class DiscordServer(Base):
	__tablename__ = "dicord_server"
	server_id = Column(String, primary_key=True)
	channel_id = Column(String)

class UserInfo(Base):
    __tablename__ = "user_info"
    line_id = Column(String, primary_key=True)
    server_id = Column(String, primary_key=True)
    auth_flag = Column(Boolean, default=False)
    text_notice = Column(Boolean, default=True)
    voice_notice = Column(Boolean, default=True)

class LineCrud:
    def __init__(self):
        self.__Session = sessionmaker(bind=engine)
        self.__session = Session() 

    def add_line_id_to_password(self, line_id):
        self.__session.add(Password(line_id=line_id))
        self.__session.commit()

def create_db():
    engine = create_engine("{}://{}:{}@{}:{}/{}"\
    			.format(os.environ["DBMS"], os.environ["USER_NAME"], os.environ["PASSWORD"], \
                os.environ["HOST"], os.environ["PORT"], os.environ["DATABASE"]), encoding="utf8", echo=True)

    Base.metadata.create_all(engine)