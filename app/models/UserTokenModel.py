from app.models import db, cfg_db_schema

class UserTokenModel(db.Model):
    __tablename__ = 'user_token'
    __table_args__ = {"schema": cfg_db_schema}
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(200), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(cfg_db_schema + '.users.id'), nullable=False)

    def __repr__(self):
        return "<UserTokenModel %r>" % (self.token)