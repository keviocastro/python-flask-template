from flask import request


def custom_parameters():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=12, type=int)
    search = request.args.get('search')

    return page, per_page, search