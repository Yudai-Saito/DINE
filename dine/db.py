#coding : utf-8
import os
import datetime
from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, not_, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("{}://{}:{}@{}:{}/{}"\
    			.format(os.environ["DBMS"], os.environ["USER_NAME"], os.environ["PASSWORD"], \
                os.environ["HOST"], os.environ["DBMS_PORT"], os.environ["DATABASE"]), encoding="utf8", echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = "user_info"
    line_id = Column(String, primary_key=True)
    discord_id = Column(String, unique=True)
    talk_server = Column(String)
    talk_time = Column(DateTime)

class Password(Base):
    __tablename__ = "password"
    line_id = Column(String, primary_key=True)
    discord_id = Column(String, unique=True)
    server_id = Column(String)
    password = Column(Integer, unique=True)
    register_time = Column(DateTime)
    pass_history = Column(Boolean, default=False)

class DiscordServer(Base):
    __tablename__ = "dicord_server"
    server_id = Column(String, primary_key=True)
    webhook_id = Column(String)
    prefix = Column(String, default="!")

class ServerInfo(Base):
    __tablename__ = "server_info"
    no = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(String)
    line_id = Column(String)
    discord_id = Column(String)
    text_notice = Column(Boolean, default=True)
    voice_notice = Column(Boolean, default=True)

class LineCrud:
    def add_following_user(self, session, line_id):
        session.add(User(line_id=line_id))

    def add_following_to_password(self, session, line_id, password):
        session.add(Password(line_id=line_id, password=password, register_time=datetime.datetime.now()))
    
    def exists_password(self, session, password):
        return session.query(session.query(Password).filter(Password.password == password).exists()).scalar()

    def exists_line_user(self, session, line_id):
        return session.query(session.query(Password).filter(Password.line_id == line_id).exists()).scalar()

    def del_userinfo_block(self, session, line_id):
        session.query(User).filter(User.line_id == line_id).delete()
        session.query(Password).filter(Password.line_id == line_id).delete()
        session.query(ServerInfo).filter(ServerInfo.line_id == line_id).delete()

    def accept_user(self, session, line_id):
        discord_id = session.query(Password.discord_id).filter(Password.line_id == line_id).scalar()
        session.query(User).filter(User.line_id == line_id).update({User.discord_id : discord_id})
        session.add(ServerInfo(line_id=line_id, discord_id=discord_id,\
                                server_id=session.query(Password.server_id).filter(Password.line_id == line_id).scalar()))
        session.query(Password).filter(Password.line_id == line_id).delete()

    def get_server_id(self, session, line_id):
        return session.query(ServerInfo.server_id).filter(ServerInfo.line_id == line_id).all()

    def delete_server(self, session, line_id, server_id):
        session.query(ServerInfo).filter(ServerInfo.line_id == line_id, ServerInfo.server_id == server_id).delete()

        discord_server = session.query(ServerInfo.server_id).filter(ServerInfo.line_id == line_id).all()
        if len(discord_server) == 1:
            session.query(User).filter(User.line_id == line_id).update({User.talk_server : discord_server[0][0]})
        else:
            session.query(User).filter(User.line_id == line_id, User.talk_server == server_id).update({User.talk_server : None})

    def get_server_text(self, session, line_id, server_id):
        return session.query(ServerInfo.text_notice).filter(ServerInfo.line_id == line_id, ServerInfo.server_id == server_id).scalar()

    def get_server_voice(self, session, line_id, server_id):
        return session.query(ServerInfo.voice_notice).filter(ServerInfo.line_id == line_id, ServerInfo.server_id == server_id).scalar()

    def setting_server_text(self, session, line_id, server_id):
        session.query(ServerInfo).filter(ServerInfo.line_id == line_id, ServerInfo.server_id == server_id).\
                    update({ServerInfo.text_notice : not_(ServerInfo.text_notice)})

        return session.query(ServerInfo.text_notice).filter(ServerInfo.line_id == line_id, ServerInfo.server_id == server_id).scalar()
    
    def setting_server_voice(self, session, line_id, server_id):
        session.query(ServerInfo).filter(ServerInfo.line_id == line_id, ServerInfo.server_id == server_id).\
                    update({ServerInfo.voice_notice : not_(ServerInfo.voice_notice)})

        return session.query(ServerInfo.voice_notice).filter(ServerInfo.line_id == line_id, ServerInfo.server_id == server_id).scalar()
        
    def set_user_info(self, session, line_id):
        discord_server = session.query(ServerInfo.server_id).filter(ServerInfo.line_id == line_id).all()
        if len(discord_server) == 1:
            session.query(User).filter(User.line_id == line_id).update({User.talk_server : discord_server[0][0]})
        else:
            session.query(User).filter(User.line_id == line_id).update({User.talk_server : None})
            
    def set_user_talk_server(self, session, line_id, server_id):
        user_stat = session.query(session.query(ServerInfo).filter(ServerInfo.line_id == line_id, ServerInfo.server_id == server_id).exists()).scalar()
        if user_stat == True:
            session.query(User).filter(User.line_id == line_id).update({User.talk_server : server_id})
            return True
        else:
            return False
    def get_discord_user(self, session, line_id):
        return session.query(User.discord_id).filter(User.line_id == line_id).scalar()

    def get_webhook_id(self, session, line_id):
        user_join_stat = session.query(session.query(ServerInfo).filter(ServerInfo.line_id == line_id).exists()).scalar()

        if user_join_stat == True: 
            talk_server = session.query(User.talk_server).filter(User.line_id == line_id).scalar()

            if talk_server == None:
                return None
            else:
                return session.query(DiscordServer.webhook_id).filter(DiscordServer.server_id == talk_server).scalar()
        else:
            return False
            
    def set_talk_time(self, session, line_id):
        session.query(User).filter(User.line_id == line_id).update({User.talk_time : datetime.datetime.now()})

class DiscordCrud:
    def add_join_server(self, session, server_id):
        session.add(DiscordServer(server_id=server_id))
    
    def exists_user(self, session, server_id, discord_id):
        return session.query(session.query(ServerInfo).filter(ServerInfo.server_id == str(server_id), ServerInfo.discord_id == str(discord_id)).exists()).scalar()

    def exists_password(self, session, password):
        return session.query(session.query(Password).filter(Password.password == password, Password.pass_history == False).exists()).scalar()

    def register_user(self, session, password):
        return session.query(Password.line_id).filter(Password.password == password).scalar()
    
    def add_register_to_password(self, session, password, discord_id, server_id):
        session.query(session.query(Password).filter(Password.password == password).\
                    update({Password.discord_id : discord_id, Password.server_id : server_id, Password.pass_history : True}))

    def set_prefix(self, session, server_id, prefix):
        session.query(session.query(DiscordServer).filter(DiscordServer.server_id == str(server_id)).update({DiscordServer.prefix : prefix}))

    def get_prefix(self, session, server_id):
        return session.query(DiscordServer.prefix).filter(DiscordServer.server_id == str(server_id)).scalar()
    
    def set_webhook_id(self, session, server_id, webhook_id):
        session.query(DiscordServer).filter(DiscordServer.server_id == server_id).update({DiscordServer.webhook_id : webhook_id})

    def get_webhook_id(self, session, server_id):
        return session.query(DiscordServer.webhook_id).filter(DiscordServer.server_id == server_id).one()

    def delete_server(self, session, server_id):
        session.query(DiscordServer).filter(DiscordServer.server_id == server_id).delete()

    def get_line_id(self, session, server_id, discord_ids):
        return session.query(ServerInfo.line_id).filter(ServerInfo.server_id == server_id, ServerInfo.discord_id.in_(discord_ids), ServerInfo.text_notice == True).all()


class ScheduleManager():
    def time_over_user(self, session):
        nowtime = datetime.datetime.now()
        session.query(Password).filter(Password.register_time < nowtime - datetime.timedelta(minutes=5)).delete()

        session.query(User).filter(User.talk_time < nowtime - datetime.timedelta(minutes=5), User.line_id.in_(session.query(ServerInfo.line_id).\
            group_by(ServerInfo.line_id).having(func.count(ServerInfo.line_id) > 1))).update({User.talk_server : None}, synchronize_session="fetch")

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