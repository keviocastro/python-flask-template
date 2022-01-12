import uuid

from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app import db
from app.admin.city.models import City
from app.services.aws.s3 import get_aws_image_keys_private
from app.services.sqlalchemy.models import BaseModel

"""
Credential levels

1 - System / Sistema (desenvolvedores)
2 - Admin
3 - Editor
4 - Autor
5 - Client
"""


class User(db.Model, BaseModel):
    __tablename__ = "user"

    hash_id = db.Column(db.String(36), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=0)
    token_update = db.Column(db.String(36))
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    image_key = db.Column(db.String(256))
    taxpayer = db.Column(db.String(256))
    genre = db.Column(db.String(256))
    cell_phone = db.Column(db.String(256))
    birth_date = db.Column(db.Date)
    status = db.Column(db.Boolean, default=1)

    # ForeignKeys
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    group = db.relationship('Group', backref='user', lazy=True, uselist=False)

    def _get_image(self):
        return get_aws_image_keys_private(self.image_key)

    image = property(_get_image)

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def check_password(self, candidate):
        return pbkdf2_sha256.verify(candidate, self.password)

    def create_item(self, dict_model):
        self.hash_id = str(uuid.uuid4())
        self.email = dict_model.get("email", self.email)
        self.set_password(dict_model["password"])
        self.token_update = str(uuid.uuid4())
        self.name = dict_model.get("name", self.name)
        self.taxpayer = dict_model.get("taxpayer", self.taxpayer)
        self.genre = dict_model.get("genre", self.genre)
        self.cell_phone = dict_model.get("cell_phone", self.cell_phone)
        self.birth_date = dict_model.get("birth_date", self.birth_date)
        try:
            self.group_id = dict_model["group_id"]
        except:
            self.group_id = 5

        return self

    def update_item(self, dict_model):
        try:
            self.set_password(dict_model["password"])
        except:
            pass
        self.name = dict_model.get("name", self.name)
        self.genre = dict_model.get("genre", self.genre)
        self.cell_phone = dict_model.get("cell_phone", self.cell_phone)
        self.birth_date = dict_model.get("birth_date", self.birth_date)
        self.status = dict_model.get("status", self.status)
        self.group_id = dict_model.get("group_id", self.group_id)
        return self


class UserAddress(db.Model, BaseModel):
    __tablename__ = "user_address"

    code_post = db.Column(db.String(256))
    street = db.Column(db.String(256))
    number = db.Column(db.String(256))
    district = db.Column(db.String(256))
    complement = db.Column(db.String(256))

    lat = db.Column(db.String(256))
    long = db.Column(db.String(256))

    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    city = db.relationship(City, uselist=False, backref="user_address")

    def create_item(self, model_dict):
        self.code_post = model_dict["code_post"]
        self.street = model_dict["street"]
        self.number = model_dict["number"]
        self.district = model_dict["district"]
        self.complement = model_dict["complement"]
        self.lat = model_dict.get("lat", None)
        self.long = model_dict.get("long", None)
        self.user_id = model_dict["user_id"]
        self.city_id = model_dict["city"]["id"]

        return self

    def update_item(self, model_dict):
        self.code_post = model_dict["code_post"]
        self.street = model_dict["street"]
        self.number = model_dict["number"]
        self.district = model_dict["district"]
        self.complement = model_dict["complement"]
        self.lat = model_dict.get("lat", self.lat)
        self.long = model_dict.get("long", self.long)
        self.city_id = model_dict["city"]["id"]

        return self
