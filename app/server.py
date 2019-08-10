from flask import Flask, escape, request, Response
import settings

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/swagger.yaml')
def swagger():
    with open("openapi.yaml", "r") as file:
        resp = Response(file.read())

    if settings.DEBUG:
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
