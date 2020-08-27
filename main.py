import random
import io
from PIL import Image
import requests
import sys
import json
import patterns
from flask.globals import request

from collections import namedtuple
from flask import Flask, jsonify, send_file, render_template, abort, make_response, send_from_directory

# Checking if you have config.json on your API
try:
    with open("config.json", encoding='utf-8') as data:
        config = json.load(data, object_hook=lambda d: namedtuple(
            'X', d.keys())(*d.values()))
except FileNotFoundError:
    print("You need to make a config file to be able to run this API")
    sys.exit()


app = Flask(__name__)


# region routes


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


@app.route("/api/v1/discordmsg", methods=["GET"])
def jsonSpecs():
    output = {
        "user": "the username",
        "message": "text to display",
        "picture": "link of the photo",
        "color": "hex user color default gray"
    }
    return jsonify(output)


@app.route("/random")
def getRandom():
    lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Donec molestie ante nulla, vitae finibus enim auctor in.
Nam blandit eleifend ex, laoreet dapibus turpis porta id. Vivamus 
suscipit id enim nec vulputate. Integer mattis, 
leo eu accumsan dictum, nulla odio ultrices odio, quis pretium 
lacus est quis est. In fermentum diam nec 
sem consequat, a aliquet ante euismod. Ut vitae ornare mi, 
non fringilla lorem.""".split(' ')

    defaultPic = Image.open("templates/images/defaultPicture.png")

    task = {
        'picture': defaultPic,
        'message': " ".join(lorem[random.randrange(0, 31):random.randrange(31, 62)]),
        'user': random.choice(lorem).strip(),
        'color': "#8e9b9b"
    }

    patternAppliedImg = patterns.discordMsg(**task)

    return _serve_pil_image(patternAppliedImg)


@app.route("/assets/images/<path:path>")
def template_images(path):
    print(path)
    return send_from_directory("templates/images", path)

# endregion


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(port=config.port, debug=config.debug, threaded=True)
