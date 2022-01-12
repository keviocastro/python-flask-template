from app.admin.user.models import User


def select_user_by_jwt(user_jwt):
    return User.query.filter(User.hash_id == user_jwt["hash_id"], User.status == 1, User.deleted_at == None).first()