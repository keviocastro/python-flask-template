from flask import request
from flask_jwt_extended import jwt_required

from app.admin.city import bp
from app.admin.city.services.crud import get_city, update_city, delete_city, \
    gets_city, \
    create_city
from app.services.requests.intercept import intercept_admin_user
from app.services.requests.requests import default_return


@bp.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
@intercept_admin_user
def item(id):
    try:
        if request.method == 'GET':
            item = get_city(id, True)
            return default_return(200, 2, item)

        if request.method == 'PUT':
            item = update_city(id, True)
            return default_return(200, 3, item)

        if request.method == 'DELETE':
            delete_city(id)
            return default_return(204, 4)
    except Exception as e:
        raise e


@bp.route('', methods=['GET', 'POST'])
@jwt_required()
@intercept_admin_user
def items():
    try:
        if request.method == 'GET':
            items, items_paginate = gets_city(True)
            return default_return(200, 2, items, items_paginate)

        if request.method == 'POST':
            item = create_city(schema=True)
            return default_return(201, 1, item)

    except Exception as e:
        raise e
