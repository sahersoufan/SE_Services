from Class.seCore import seCore
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'this is my first api'

@app.route('/post', methods=["POST"])
def post():
    input_json = request.get_json(force=True)
    dictToReturn = {'data':input_json['data']}
    return jsonify(dictToReturn['data'])

@app.route('/initializeSE', methods=['GET'])
def initiate():
    seCore.initiate()
    return 'bla bla'
@app.route('/updateSE', methods=['GET'])
async def update():
    await seCore.update()
    return 'bla bla'

@app.route('/getS', methods=['POST'])
def getRecommend():
    query = request.get_json(force=True)
    r = seCore.getS(query)
    return jsonify(r)


app.run(port=3001)