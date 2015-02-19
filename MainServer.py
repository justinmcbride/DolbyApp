from flask import Flask, jsonify, request
import FileHandler as fh

server = Flask(__name__)

'''
The main page of the API.
Return a list of all files on the server, along with their ID.
'''
@server.route('/')
def MainPage():
    return formatResponse(fh.GetAllFiles())

'''
This route will be used to retrieve, modify, or delete a file on the server.
'''
@server.route('/file/<int:fileID>', methods=['GET', 'PUT', 'DELETE'])
def singleFile(fileID):
    json = request.json

    if request.method == 'GET':
        return formatResponse({"passedInt": fileID})
    elif request.method == 'PUT':
        if not json:
            return notJSON()
    elif request.method == 'DELETE':
        return formatResponse("Deleted")

    return formatResponse({"passedInt": fileID})

'''
This route will be used to create a new file on the server.
'''
@server.route('/file', methods=['POST'])
def createFile():
    json = request.json
    if not json:
        return notJSON()

'''
To create an always parseable response,
run all responses through this function
'''
def formatResponse(data, error=False):
    return jsonify(data = data, error=error)

'''
Respond with the fact that JSON was expected
'''
def notJSON():
    return formatResponse("Expected JSON data. Ensure Content-Type header is sent.", error=True)

if __name__ == '__main__':
    server.debug = True
    server.run()

# TODO: allow cli of host and port address