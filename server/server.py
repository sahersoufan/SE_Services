from Class.seCore import seCore, seCoreV2
from flask import Flask, jsonify, request


myPort = 8051
app = Flask(__name__)


# @app.route('/setSqlInfo', methods=["POST"])
# def setSqlInfo():
#     try:
#         sqlInfo = request.get_json(force=True)
#         seCore.setSqlInfo(sqlInfo)
#         return jsonify(success=True)
#     except:
#         return jsonify(success=False)


# @app.route('/initializeSE', methods=['POST'])
# def initiate():
#     try:
#         seCore.initiate()
#         return jsonify(success=True)
#     except:
#         return jsonify(success=False)


# @app.route('/updateSE', methods=['GET'])
# async def update():
#     try:
#         await seCore.update()
#         return jsonify(success=True)
#     except:
#         return jsonify(success=False)


# @app.route('/getS', methods=['POST'])
# def getS():
#     try:
#         query = request.get_json(force=True)
#         r = seCore.getS(query)
#         return jsonify(r)
#     except:
#         raise
        # return jsonify(success=False)



###############################################################
#                     EMBEDDING
###############################################################
@app.route('/setSqlInfo', methods=["POST"])
def setSqlInfo():
    try:
        sqlInfo = request.get_json(force=True)
        seCoreV2.setSqlInfo(sqlInfo)
        return jsonify(success=True)
    except:
        return jsonify(success=False)


@app.route('/initializeSE', methods=['POST'])
def initiate():
    try:

        seCoreV2.initiate()
        return jsonify(success=True)
    except:
        return jsonify(success=False)

@app.route('/updateSE', methods=['POST'])
async def update():
    try:
        await seCoreV2.update()
        return jsonify(success=True)
    except:
        return jsonify(success=False)


@app.route('/getS', methods=['GET'])
def getS():
    try:
        query = request.get_json(force=True)
        r = seCoreV2.getS(query)
        return jsonify(r)
    except:
        raise


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=myPort)