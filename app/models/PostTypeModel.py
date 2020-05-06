from datetime import datetime

from app.models import db, ma, cfg_db_schema


class PostTypeModel(db.Model):
    __tablename__ = 'post_type'
    __table_args__ =  {'schema': cfg_db_schema}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def  __repr__(self):
        return "<PostType %r>" % (self.name)