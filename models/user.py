from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from db import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nickname = db.Column(db.String(80), nullable=False)
    pwd = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, nickname, password):
        self.email = email
        self.nickname = nickname
        self.pwd = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd, password)

    def get_id(self):
        return str(self.id)


# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
# from db import dynamodb

# class User(UserMixin):
#     def __init__(self, email, nickname, password):
#         self.email = email
#         self.nickname = nickname
#         self.pwd = generate_password_hash(password)
#         self.created_at = datetime.utcnow().isoformat()
#         self._id = email  # use 'email' as primary key

#     @staticmethod
#     def get_table():
#         return dynamodb.Table('users')

#     def save(self):
#         table = self.get_table()
#         table.put_item(Item={
#             'email': self.email,
#             'nickname': self.nickname,
#             'pwd': self.pwd,
#             'created_at': self.created_at
#         })

#     @classmethod
#     def get_by_email(cls, email):
#         table = cls.get_table()
#         response = table.get_item(Key={'email': email})
#         item = response.get('Item')
#         if item:
#             user = cls(email=item['email'], nickname=item['nickname'], password='')
#             user.pwd = item['pwd']  # Directly set the password that has been hashed
#             user.created_at = item['created_at']
#             return user
#         return None

#     def check_password(self, password):
#         return check_password_hash(self.pwd, password)

#     def get_id(self):
#         return self.email  # use 'email' as user's ID