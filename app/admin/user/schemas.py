from marshmallow import fields

from app import ma
from app.services.sqlalchemy.schemas import ReducedSchema


class UserConfigSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("notification_new_image", "notification_new_category", "notification_new_collection", "notification_promotion")
        ordered = True


class UserPaymentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name")
        ordered = True


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "hash_id", "name", "email", "status", "cpf", "cell_phone", "image", "config", "group")
        ordered = True

    config = fields.Nested(UserConfigSchema())
    group = fields.Nested(ReducedSchema())
