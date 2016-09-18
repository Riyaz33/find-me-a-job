#!/usr/bin/env python
from flask import abort, Flask, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from helpers.analyze_results import analyze_results
from helpers.find_all_documents import find_all_documents

import string
import random

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            fn, ext = secure_filename(file.filename).rsplit('.', 1)

            filename = '%s.%s' % (id_generator(8), ext)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print(filepath.rsplit('/', 1))
            return redirect(url_for('show_results', f=filepath.rsplit('/', 1)[1]))

        return redirect(url_for('upload_file'))
    else:
        return render_template('upload.html')


@app.route('/results')
def show_results():
    fp = 'static/uploads/%s' % request.args.get('f')
    res = analyze_results(fp)

    if not res:
        abort(400)

    cleansed_docs = dict()

    all_docs = find_all_documents()
    for doc in all_docs:
        cleansed_docs[doc['name']] = doc

    return render_template('results.html',
                           data=res,
                           all_docs=cleansed_docs)


@app.errorhandler(400)
@app.errorhandler(403)
@app.errorhandler(404)
def bad_request(error):
    response = jsonify(meta=dict(status=error.code, message=error.description))
    # return response, error.code
    return redirect(url_for('index'))

if __name__ == '__main__':
    import os

    HOST, PORT, DEBUG = os.environ.get('HOST', '0.0.0.0'), \
        os.environ.get('PORT', 3000), \
        os.environ.get('DEBUG', False)
    app.run(host=HOST, port=int(PORT), debug=DEBUG)
