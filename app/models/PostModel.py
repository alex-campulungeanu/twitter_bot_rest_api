from datetime import datetime

from app.models import db, ma, cfg_db_schema
from app.models.UserModel import UserSchema
from app.models.PlatformModel import PlatformModel
from app.models.PostPlatformModel import PostPlatformModel

# post_platform = db.Table('post_platform',
#     db.Column('post_id', db.Integer, db.ForeignKey(cfg_db_schema + '.post.id'), primary_key=True),
#     db.Column('platform_id', db.Integer, db.ForeignKey(cfg_db_schema + '.platform.id'), primary_key=True),
#     db.Column('created_at', db.DateTime, default=datetime.utcnow),
#     ## or for multiple PK db.PrimaryKeyConstraint('post_id', 'platform_id')
#     schema=cfg_db_schema
# )

class PostModel(db.Model):
    __tablename__ = 'post'
    __table_args__ =  {'schema': cfg_db_schema}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text, nullable=False)
    post_type_id = db.Column(db.Integer, db.ForeignKey(cfg_db_schema + '.post_type.id'), nullable=False, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey(cfg_db_schema + '.users.id'), nullable=False)
    user = db.relationship("UserModel", backref=db.backref("posts", lazy="dynamic"))
    # platforms = db.relationship('PlatformModel', secondary=post_platform, backref='platform_posts')
    platform = db.relationship('PostPlatformModel', back_populates='post') 
    md5 = db.Column(db.Text, nullable=False, index=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)

    def  __repr__(self):
        return "<Post %r>" % (self.id)

class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PostModel
        fields = ("id", "name")
    # id = ma.auto_field()
    # name = ma.auto_field()
    # # body = ma.auto_field()
    # user = ma.Nested(UserSchema, dump_only=True)