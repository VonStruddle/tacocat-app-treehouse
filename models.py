import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from peewee import *


DB = SqliteDatabase('tacocat.db')


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DB

    @classmethod
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
    cheese = BooleanField(default=False)
    shell = CharField()
    extras = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DB
        order_by = ('-created_at',)


def initializeDB():
    DB.connect()
    DB.create_tables([User, Taco], safe=True)
    DB.close()
