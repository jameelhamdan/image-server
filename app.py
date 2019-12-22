from flask import Flask, request, abort, send_from_directory
import utils
import uuid
import os

app = Flask(__name__)
UPLOAD_FOLDER = './static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_is_a_secret_key_please_keep_it_very_secret')


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


@app.route('/image/<string:token>', methods=['GET'])
def get_image(token):

    if not utils.verify_token(token):
        abort(401)

    image_uuid = utils.verify_token(token)

    if not utils.check_if_file_exists(image_uuid):
        abort(404)

    return send_from_directory(app.config['UPLOAD_FOLDER'], '{}.png'.format(image_uuid), as_attachment=False)


if __name__ == '__main__':
    app.run()
