from app import db
from app.services.sqlalchemy.models import BaseModel


class Group(db.Model, BaseModel):
    __tablename__ = 'group'

    name = db.Column(db.String(256))
    status = db.Column(db.Boolean, default=1)

    def create_item(self, dict_model):
        self.name = dict_model['name']
        return self

    def update_item(self, dict_model):
        self.name = dict_model.get('name', self.name)
        self.status = dict_model.get('status', self.status)
        return self
