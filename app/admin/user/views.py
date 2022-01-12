from flask import request
from flask_jwt_extended import jwt_required

from app.admin.user import bp
from app.admin.user.services.crud import get_user, update_user, delete_user, \
    gets_user, \
    create_user
from app.admin.user.services.image import create_user_image
from app.services.requests.intercept import intercept_admin_user
from app.services.requests.requests import default_return


@bp.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
@intercept_admin_user
def item(id):
    if request.method == 'GET':
        try:
            item = get_user(id, True)
            return default_return(200, 2, item)
        except Exception as e:
            raise e

    if request.method == 'PUT':
        try:
            item = update_user(id, True)
            return default_return(200, 3, item)
        except Exception as e:
            raise e

    if request.method == 'DELETE':
        try:
            delete_user(id)
            return default_return(204, 4)
        except Exception as e:
            raise e


@bp.route('', methods=['GET', 'POST'])
@jwt_required()
@intercept_admin_user
def items():
    if request.method == 'GET':
        try:
            items, items_paginate = gets_user(True)
            return default_return(200, 2, items, items_paginate)
        except Exception as e:
            raise e

    if request.method == 'POST':
        try:
            item = create_user(schema=True)
            return default_return(201, 1, item)
        except Exception as e:
            raise e


@bp.route('/<id>/images')
@jwt_required()
@intercept_admin_user
class UserResourceImage():

    def post(self, id):
        try:
            item = get_user(id)
            image_return = create_user_image(item)
            return default_return(200, 2, image_return)
        except Exception as e:
            raise e
