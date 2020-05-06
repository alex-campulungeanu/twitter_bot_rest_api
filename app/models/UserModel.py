from datetime import datetime
from time import time
import jwt
import os

from werkzeug.security import check_password_hash, generate_password_hash

from app.models import db, ma, cfg_db_schema
from app.models.RoleModel import RoleModel
from app import app

user_role = db.Table('users_role',
    db.Column('user_id', db.Integer, db.ForeignKey(cfg_db_schema + '.users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey(cfg_db_schema + '.role.id')),
    schema=cfg_db_schema
)

class UserModel(db.Model):
    __tablename__ = 'users'
    __table_args__ = {"schema": cfg_db_schema}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship('RoleModel', secondary=user_role)
    # tokens = db.relationship('UserTokenModel', backref='user_token', lazy=True)
    # roles = db.relationship('RoleModel', secondary=user_role, lazy='subquery',
    #                             backref=db.backref('role', lazy=True))
    # posts = db.relationship('PostModel', backref='user_posts', lazy=True)
    

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        # return self.password_hash == password
        return check_password_hash(self.password, password)
    
    def get_forgot_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['JWT_RESET_PASSWORD_KEY'],
            algorithm='HS256'
        ).decode('utf-8')
    
    @staticmethod
    def verify_forgot_password(token):
        try:
            id = jwt.decode(token, app.config['RESET_PASSWORD_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return UserModel.query.get(id)
    
    def __repr__(self):
        return "<User %r>" % (self.email)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        # fields = ("id", "name", )
    id = ma.auto_field()
    email = ma.auto_field()
    name = ma.auto_field()