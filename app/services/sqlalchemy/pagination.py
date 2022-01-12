def pagination_info(pagination_result):
    """Return pagination info"""

    try:
        info = {
            "has_next": pagination_result.has_next,
            "has_prev": pagination_result.has_prev,
            "current_page": pagination_result.page,
            "total_items": pagination_result.total,
            "total_pages": pagination_result.pages
        }
    except:
        info = {}

    return info
