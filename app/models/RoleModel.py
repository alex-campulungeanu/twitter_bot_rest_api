from app.models import db, cfg_db_schema

from app.models import PermissionModel

role_permission = db.Table('role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey(cfg_db_schema + '.role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey(cfg_db_schema + '.permission.id')),
    schema=cfg_db_schema
)

class RoleModel(db.Model):
    __tablename__ = 'role'
    __table_args__ = {'schema': cfg_db_schema}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.relationship('PermissionModel', secondary=role_permission)

    def __repr__(self):
        return "<Role %r>" % (self.name)