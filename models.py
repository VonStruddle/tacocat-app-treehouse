import datetime

from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash
from peewee import *


DB = SqliteDatabase('tacocat.db')


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DB

    @staticmethod
    def create_user(cls, email, password):
        try:
            with DB.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError('User already exists')


class Taco(Model):
    user = ForeignKeyField(
        rel_model=User,
        related_name='tacos'
    )
    protein = CharField()
    cheese = BooleanField()
    shell = CharField()
    extras = TextField()