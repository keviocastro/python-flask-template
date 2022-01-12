import uuid
from flask import request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.admin.user.models import User
from app.admin.user.schemas import UserSchema
from app.admin.user.services.crud import validate_email
from app.client import bp
from app.services.aws.email import EmailService
from app.services.aws.s3 import upload_file_s3, delete_file_s3, \
    get_aws_image_keys_private
from app.services.errors.exceptions import UnauthorizedError
from app.services.requests.requests import default_return
from app.services.utils import code_generator
from app.services.utils.image import get_base64_image
from config import Config


def get_client_by_hash(hash_id, columns=False):
    query = User.query
    if columns:
        query = query.with_entities(
            *[getattr(User, column) for column in columns])
    user = query.filter(User.hash_id == hash_id).first()
    return user


@bp.route('', methods=['POST'])
@jwt_required()
def client_create():
    if request.method == 'POST':
        dict_body = request.get_json()
        dict_body["group_id"] = 5

        if validate_email(dict_body["email"]):
            raise UnauthorizedError('Usuário com este e-mail já existe!')

        try:
            item = User().create_item(dict_body).save()
        except:
            raise Exception

        return default_return(201, 1, UserSchema(exclude=["id"]).dump(item))


@bp.route('', methods=['GET', 'PUT'])
@jwt_required()
def client():
    if request.method == 'GET':
        user_jwt = get_jwt_identity()
        item = get_client_by_hash(user_jwt["hash_id"])
        return default_return(200, 2,
                              UserSchema(exclude=["id"]).dump(item))

    if request.method == 'PUT':
        user_jwt = get_jwt_identity()
        item = get_client_by_hash(user_jwt["hash_id"])
        dict_body = request.get_json()
        item.update_item(dict_body).update()
        return default_return(200, 2,
                              UserSchema(exclude=["id"]).dump(item))


@bp.route('/image', methods=['POST'])
@jwt_required()
def image():
    if request.method == 'POST':
        user_jwt = get_jwt_identity()
        item = get_client_by_hash(user_jwt["hash_id"])

        dict_body = request.get_json()
        image, ext = get_base64_image(dict_body['image'])
        upload = upload_file_s3(image, f'images/users/{item.hash_id}',
                                f'{str(uuid.uuid1())}{ext}')

        try:
            delete_file_s3(item.image_key)
        except:
            pass

        try:
            image_key = upload['image_key']
            item.image_key = image_key
            item.update()
            image_return = get_aws_image_keys_private(image_key)
        except:
            pass

        return default_return(200, 2, image_return)


@bp.route('/recover', methods=['POST'])
def recover():
    if request.method == 'POST':
        dict_body = request.get_json()
        email = dict_body['email']
        item = User.query.filter(User.email == email).first()

        if item:

            password = code_generator(6)

            # ATUALIZA TOKEN
            token = uuid.uuid1()
            item.set_password(password)
            item.token_update = str(token)
            item.update()

            # ENVIAR EMAIL PARA RECUPERAR SENHA
            to = item.email
            subject = "Solicitação para configurar nova senha"

            body = render_template('email/reset.html', name=item.name,
                                   email=to, password=password,
                                   url_confirm=f'{Config.SITE_HTTPS}/minha-conta/resetar-senha?hash={token}')

            EmailService().send_aws(to, subject, body)

            msg = "E-mail enviado com Sucesso! Verifique sua caixa de e-mail!"
            return default_return(200, msg)
        else:
            raise UnauthorizedError('Usuário não encontrado!')
