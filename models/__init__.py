import uuid
from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def generate_uuid_str():
    return str(uuid.uuid1())


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(192), default=generate_uuid_str, primary_key=True, )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, index=True)

# https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
