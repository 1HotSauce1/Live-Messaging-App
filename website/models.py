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

    def __init__(self, user_id1, user_id2):
        self.user_id1 = user_id1
        self.user_id2 = user_id2

    def get_id(self):
           return (self.friendship_id)

