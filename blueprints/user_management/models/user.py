from werkzeug.security import generate_password_hash, check_password_hash

from models import BaseModel
from models import db


# from sqlalchemy import Column, ForeignKey


class User(BaseModel):
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update(self, **kwargs):
        name = kwargs.get('name', self.name)
        email = kwargs.get('email', self.email)
        password = kwargs.get('password')

        self.name = name
        self.email = email

        if password:
            self.set_password(password)

    @property
    def serialize(self):
        return dict(
            id=self.id,
            name=self.name,
            email=self.email
        )

    def __repr__(self):
        return '<User %r>' % self.name
