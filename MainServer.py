from flask import Flask, jsonify, request

server = Flask(__name__)

@server.route('/')
def MainPage():
    return formatResponse("MainPage")

@server.route('/file/<int:fileID>', methods=['GET', 'PUT', 'DELETE'])
def singleFile(fileID):
    json = request.json

    if request.method == 'GET':
        return formatResponse({"passedInt": fileID})
    elif request.method == 'PUT':
        if not json:
            return formatResponse("Expected JSON data. Ensure Content-Type header is sent.", error=True)
    elif request.method == 'DELETE':
        return formatResponse("Deleted")

    return formatResponse({"passedInt": fileID})


'''
To create an always parseable response,
run all responses through this function
'''

def formatResponse(data, error=False):
    return jsonify(data = data, error=error)


if __name__ == '__main__':
    server.debug = True
    server.run()

# TODO: allow cli of host and port address