from flask import Flask, request, abort
import keys
import utils
import uuid
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'upload')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PRIVATE_KEY'] = os.environ.get('PRIVATE_KEY', keys.private_key)
app.config['PUBLIC_KEY'] = os.environ.get('PUBLIC_KEY', keys.public_key)


@app.route('/upload', methods=['POST'])
def upload_image():
    new_uuid = '{}{}'.format(uuid.uuid4(), uuid.uuid4())
    try:
        utils.upload_file(request, new_uuid)
    except utils.ValidationError as e:
        return utils.json_response(
            ({
                'message': 'Image Upload Failed : {}'.format(e),
            }), 400
        )

    return utils.json_response({
        'message': 'Image Uploaded Successfully',
        'uuid': new_uuid,
    })


@app.route('/get/<string:image_uuid>/<string:token>', methods=['GET'])
def get_image(image_uuid, token):
    if not utils.check_if_file_exists(image_uuid):
        abort(404)

    if not utils.verify_token(token, image_uuid):
        abort(401)

    ## code here to actually serve image
    return ''


if __name__ == '__main__':
    app.run()


