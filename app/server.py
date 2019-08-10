from flask import Flask, Response, request
import settings
from provider import CSVProvider
import io
from processor import Processor
import psycopg2

app = Flask(__name__)


@app.route('/upload', methods=['OPTIONS', 'POST'])
def upload():
    resp = Response()
    if settings.DEBUG:
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = '*'

    if request.method == 'OPTIONS':
        return resp
    provider = CSVProvider(io.StringIO(request.data.decode("utf-8")))
    with psycopg2.connect(**settings.DB_CONFIG) as conn:
        processor = Processor(conn, "test", provider.columns(), provider.rows())
        processor.create()
        processor.insert()

    return resp


@app.route('/swagger.yaml')
def swagger():
    with open("openapi.yaml", "r") as file:
        resp = Response(file.read())

    if settings.DEBUG:
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

