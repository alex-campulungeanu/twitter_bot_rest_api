from datetime import datetime

from app.models import db, cfg_db_schema, PostPlatformModel


class PlatformModel(db.Model):
    __tablename__ = 'platform'
    __table_args__ =  {'schema': cfg_db_schema}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    posts = db.relationship('PostPlatformModel', back_populates='platform')

    def  __repr__(self):
        return "<Platform %r>" % (self.name)