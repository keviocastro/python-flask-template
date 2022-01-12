from flask import request
from sqlalchemy import asc, desc


def custom_filters():
    order_by_direction = request.args.get("order_by_direction", default="desc", type=str)
    order_by_direction = asc if order_by_direction == "asc" else desc

    return {
        "page": request.args.get("page", default=1, type=int),
        "per_page": request.args.get("per_page", default=12, type=int),
        "search": request.args.get("search"),
        "created_at_start": request.args.get("created_at_start", default=None),
        "created_at_end": request.args.get("created_at_end", default=None),
        "order_by_column": request.args.get("order_by_column", default="id", type=str),
        "order_by_direction": order_by_direction
    }
