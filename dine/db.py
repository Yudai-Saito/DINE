#coding : utf-8
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
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
    def __init__(self):
        self.__Session = sessionmaker(bind=engine)
        self.__session = self.__Session() 

    def add_following_to_password(self, line_id, password):
        self.__session.add(Password(line_id=line_id, password=password))
        self.__session.commit()
    
    def exists_password(self, password):
        return self.__session.query(self.__session.query(Password).filter(Password.password == password).exists()).scalar()

    def exists_line_user(self, line_id):
        return self.__session.query(self.__session.query(Password).filter(Password.line_id == line_id).exists()).scalar()

def create_db():
    Base.metadata.create_all(engine)