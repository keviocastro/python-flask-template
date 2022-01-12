import uuid
from flask import request

from app.services.aws.s3 import get_aws_image_keys_private, upload_file_s3, delete_file_s3
from app.services.utils.image import get_base64_image


def create_user_image(item):
    dict_body = request.get_json()
    image, ext = get_base64_image(dict_body['image'])
    upload = upload_file_s3(image, f'images/users/{item.hash_id}', f'{str(uuid.uuid1())}{ext}')

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

    return image_return
