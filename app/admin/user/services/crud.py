from flask import request
from sqlalchemy import or_

from app.admin.user.models import User
from app.admin.user.schemas import UserSchema
from app.services.errors.exceptions import NotFoundError
from app.services.requests.params import custom_parameters


def validate_email(email):
    item = User.query.filter(User.deleted_at == None, User.email==email).first()
    if item:
        return True
    else:
        return None

def create_user(schema=None):
    dict_body = request.get_json()
    item = User().create_item(dict_body).save()
    if schema:
        item = UserSchema().dump(item)
    return item


def get_user(id, schema=None, columns=None):
    query = User.query.filter(User.deleted_at == None)
    if columns:
        query = query.with_entities(*[getattr(User, column) for column in columns])
    item = query.filter(User.id == id).first()
    if not item:
        raise NotFoundError()
    if schema:
        item = UserSchema().dump(item)
    return item


def gets_user(schema=None, columns=None):
    page, per_page, search = custom_parameters()
    query = User.query.filter(User.deleted_at == None)
    if columns:
        query = query.with_entities(*[getattr(User, column) for column in columns])
    if search:
        query = query.filter(
            or_(User.name.like(f'%%{search}%%'), User.email.like(f'%%{search}%%'), User.cpf.like(f'%%{search}%%')))
    items = query.paginate(page, per_page, False)
    items_paginate = items
    if schema:
        items = UserSchema(many=True).dump(items.items)

    return items, items_paginate


def update_user(id, schema=None):
    item = get_user(id)
    dict_body = request.get_json()
    item.update_item(dict_body).update()
    if schema:
        item = UserSchema().dump(item)
    return item


def delete_user(id):
    item = get_user(id)
    item.delete()
    return True
