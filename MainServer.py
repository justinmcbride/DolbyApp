from flask import Flask, jsonify, request
import FileHandler as fh

server = Flask(__name__)

'''
The main page of the API.
Return a list of all files on the server.
'''
@server.route('/')
def MainPage():
    return formatResponse({"allFiles":fh.GetAllFiles()})

'''
This route will be used to retrieve, create, modify, or delete a file on the server.
'''
@server.route('/file/<string:filename>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def singleFile(filename):
    json = request.json

    if request.method == 'GET':
        if fh.DoesFileExist(filename):
            return formatResponse(fh.GetFile(filename))
        else:
            return formatResponse("File not found", error=True)
    elif request.method == 'PUT':
        if not json:
            return notJSON()
        if fh.DoesFileExist(filename):
            return formatResponse(fh.ModifyFile(filename, json))
        else:
            return formatResponse("File not found", error=True)
    elif request.method == 'DELETE':
        if fh.DoesFileExist(filename):
            fh.DeleteFile(filename)
            return formatResponse({"deleted": True})
        else:
            return formatResponse("File not found", error=True)
    elif request.method == 'POST':
        if not json:
            return notJSON()
        if fh.DoesFileExist(filename):
            return formatResponse("File already exists; not created", error=True)
        fh.CreateFile(filename, json)
        return formatResponse({"created" : True, "filename": filename})
    ## No need for an else, as Flask won't send other requests here


'''
This route should handle multiple files.
Retrieving, creating, modifying, and deleting.
'''
@server.route('/files', methods=['GET', 'PUT', 'DELETE', 'POST'])
def MutipleFiles():
    json = request.json
    if not json:
        return notJSON()
    if request.method == 'GET':
        # Get multiple files
    elif request.method == 'PUT':
    elif request.method == 'DELETE':
    elif request.method == 'POST':

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

# TODO: allow cli of host and port address, don't crash on empty json file while reading