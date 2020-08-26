import io
from PIL import Image
import requests
import sys
import json
import patterns
from flask.globals import request

from collections import namedtuple
from flask import Flask, jsonify, send_file, render_template, abort, make_response

# Checking if you have config.json on your API
try:
    with open("config.json", encoding='utf-8') as data:
        config = json.load(data, object_hook=lambda d: namedtuple(
            'X', d.keys())(*d.values()))
except FileNotFoundError:
    print("You need to make a config file to be able to run this API")
    sys.exit()

app = Flask(__name__)


def _serve_pil_image(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


def _downloadExternalImg(url: str) -> Image.Image:
    response: requests.Response = requests.get(url)
    im = Image.open(io.BytesIO(response.content))
    return im


@app.route("/")
def index():
    return render_template('index.html', config=config)


@app.route("/api/v1/discordmsg", methods=["POST"])
def discordMsgApi():
    conditionals = 'picture user message'.split(" ")

    hasAllConditionals = all(
        list(map(lambda x: x in request.json, conditionals)))

    if not request.json or not hasAllConditionals:
        abort(400)

    imageFile = _downloadExternalImg(request.json['picture'])

    task = {
        'picture': imageFile,
        'message': request.json.get('message', 'lorem ipsum dolor'),
        'user': request.json['user'],
        'color': request.json.get('color', "#8e9b9b")
    }
    patternAppliedImg = patterns.discordMsg(**task)
    return _serve_pil_image(patternAppliedImg)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(port=config.port, debug=config.debug)
