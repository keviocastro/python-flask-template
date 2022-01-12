from flask import request
from flask_jwt_extended import jwt_required

from app.admin.country import bp
from app.admin.country.services.crud import get_country, update_country, \
    delete_country, gets_country, \
    create_country

from app.services.requests.intercept import intercept_admin_user
from app.services.requests.requests import default_return


@bp.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
@intercept_admin_user
def item():
    if request.method == 'GET':
        try:
            item = get_country(id, True)
            return default_return(200, 2, item)
        except Exception as e:
            raise e

    if request.method == 'PUT':
        try:
            item = update_country(id, True)
            return default_return(200, 3, item)
        except Exception as e:
            raise e

    if request.method == 'DELETE':
        try:
            delete_country(id)
            return default_return(204, 4)
        except Exception as e:
            raise e


@bp.route('', methods=['GET', 'POST'])
@jwt_required()
@intercept_admin_user
def items():
    if request.method == 'GET':
        try:
            items, items_paginate = gets_country(True)
            return default_return(200, 2, items, items_paginate)
        except Exception as e:
            raise e

    if request.method == 'POST':
        try:
            item = create_country(schema=True)
            return default_return(201, 1, item)
        except Exception as e:
            raise e
