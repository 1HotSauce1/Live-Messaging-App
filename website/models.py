from . import database
from flask_login import UserMixin

class User_profiles(database.Model, UserMixin):
    __tablename__ = 'user_profiles'
    user_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(15), unique=True)
    password = database.Column(database.String(100))
    email = database.Column(database.String(30), unique=True)
    friendships = database.relationship('Friendships', foreign_keys='Friendships.user_id2')

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email
    
    def get_id(self):
           return (self.user_id)


class Friendships(database.Model):
    __tablename__ = 'friendships'
    friendship_id = database.Column(database.Integer, primary_key=True)
    user_id1 = database.Column(database.Integer, database.ForeignKey('user_profiles.user_id'))
    user_id2 = database.Column(database.Integer, database.ForeignKey('user_profiles.user_id'))
    messages = database.relationship('Chat_messages', foreign_keys='Chat_messages.friendship_id')

    def __init__(self, user_id1, user_id2):
        self.user_id1 = user_id1
        self.user_id2 = user_id2

    def get_id(self):
           return (self.friendship_id)


class Chat_messages(database.Model):
    __tablename__ = 'chat_messages'
    chat_message_id = database.Column(database.Integer, primary_key=True)
    friendship_id = database.Column(database.Integer, database.ForeignKey('friendships.friendship_id'))
    sender_id = database.Column(database.Integer)
    message = database.Column(database.String(256))

    def __init__(self, friendship_id, sender_id, message):
        self.friendship_id = friendship_id
        self.sender_id = sender_id
        self.message = message

    def get_id(self):
           return (self.chat_messages_id)

