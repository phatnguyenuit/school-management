import uuid
from datetime import datetime

from app import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(192), default=uuid.uuid1, primary_key=True, )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, index=True)

# https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
