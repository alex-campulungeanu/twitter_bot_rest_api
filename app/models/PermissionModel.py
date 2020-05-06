from flask import current_app

from app.models import db, cfg_db_schema

class PermissionModel(db.Model):
    __tablename__ = 'permission'
    __table_args__ = {"schema": cfg_db_schema}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return "<Permission %r>" % (self.name)