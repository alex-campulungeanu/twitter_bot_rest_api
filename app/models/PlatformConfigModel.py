from app.models import db, cfg_db_schema


class PlatformConfigModel(db.Model):
    __tablename__ = 'platform_config'
    __table_args__ = (db.UniqueConstraint('platform_id', 'id_config', name='unq_config_platform'), {'schema': cfg_db_schema})
    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, db.ForeignKey(cfg_db_schema + '.platform.id'), nullable=False)
    id_config = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    value = db.Column(db.String(256), nullable=False)

    def  __repr__(self):
        return "<PlatformConfig %r val: %r>" % (self.name, self.value)