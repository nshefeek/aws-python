from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
from flask_bootstrap import Bootstrap
import boto3
from filters import parse_datetime, get_filetype
from resources import get_s3_bucket, get_bucket_list



app= Flask(__name__)
Bootstrap(app)
app.jinja_env.filters['datetimeformat']  = parse_datetime
app.jinja_env.filters['file_type']  = get_filetype
app.secret_key = 'secret'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bucket = request.form['bucket']
        session['bucket'] = bucket
        return redirect(url_for('files'))
    else:
        buckets = get_bucket_list()
        return render_template("index.html", buckets=buckets)

@app.route('/files')
def files():
    s3_bucket = get_s3_bucket()
    objects = s3_bucket.objects.all()

    return render_template('files.html', bucket=s3_bucket, files=objects)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    s3_bucket = get_s3_bucket()
    s3_bucket.Object(file.filename).put(Body=file)

    flash('File uploaded successfully')
    return redirect(url_for('files'))

@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    s3_bucket = get_s3_bucket()
    s3_bucket.Object(key).delete()

    flash('File deleted successfully')    
    return redirect(url_for('files'))

@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    s3_bucket = get_s3_bucket()
    file = s3_bucket.Object(key).get()

    return Response(
        file['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition":"attachment;filename={}".format(key)}
        )

if __name__ == '__main__':
    app.run()
