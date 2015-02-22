from flask import *
import FileHandler as fh

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

def create_app(testing=False):
    app = Flask(__name__)
    from utility import ListConverter
    app.url_map.converters['list'] = ListConverter

    if testing:
        fh.setFileDir('./testingDir/')
    '''
    The main page of the API.
    Return a list of all files on the server.
    '''
    @app.route('/')
    def MainPage():
        return formatResponse({"allFiles":fh.GetAllFiles()})

    '''
    This route will be used to retrieve, create, modify, or delete a file on the server.
    '''
    @app.route('/file/<string:filename>', methods=['GET', 'PUT', 'DELETE', 'POST'])
    def singleFile(filename):
        
        if request.method == 'GET':
            if fh.DoesFileExist(filename):
                return formatResponse(fh.GetFile(filename))
            else:
                return formatResponse("File not found", error=True)
        elif request.method == 'PUT':
            json = request.json
            if not json:
                return notJSON()
            if fh.DoesFileExist(filename):
                return formatResponse(fh.ModifyFile(filename, json))
            else:
                return formatResponse("File not found; first POST the file", error=True)
        elif request.method == 'DELETE':
            if fh.DoesFileExist(filename):
                fh.DeleteFile(filename)
                return formatResponse({ "deleted": True })
            else:
                return formatResponse("File does not exist", error=True)
        elif request.method == 'POST':
            json = request.json
            if not json:
                return notJSON()
            if not filename.endswith(".json"):
                return formatResponse("Filename needs to be a .json file", error=True)
            if fh.DoesFileExist(filename):
                return formatResponse("File already exists; not created", error=True)
            fh.CreateFile(filename, json)
            return formatResponse({ "created" : True, "filename" : filename })
        ## No need for an else, as Flask won't send other requests here


    '''
    This route should handle multiple files.
    Creating and modifying.
    '''
    @app.route('/files', methods=['PUT', 'POST'])
    def MultiPostPut():
        json = request.json
        resp = {}

        if not json:
            return notJSON()

        if request.method == 'PUT':
            for filename in json:
                if fh.DoesFileExist(filename):
                    resp[filename] = { "modified" : True, "information" : fh.ModifyFile(filename, json[filename]) }
                else:
                    resp[filename] = { "modified" : False, "information" : "File does not exist; first POST it"}
        
        elif request.method == 'POST':
            for filename in json:
                if not fh.DoesFileExist(filename):
                    fh.CreateFile(filename, json[filename])
                    resp[filename] = { "created" : True }
                else:
                    resp[filename] = { "created" : False, "reason" : "File already exists" }
        return formatResponse(resp)
    
    @app.route('/files/<list:files>', methods=['GET', 'DELETE'])
    def MultiGetDelete(files):
        resp = {}
        if request.method == 'GET':
            for filename in files:
                if fh.DoesFileExist(filename):
                    resp[filename] = fh.GetFile(filename)
                else:
                    resp[filename] = "File does not exist"
        elif request.method == 'DELETE':
           for filename in files:
                if fh.DoesFileExist(filename):
                    fh.DeleteFile(filename)
                    resp[filename] = { "deleted" : True }
                else:
                    resp[filename] = { "deleted" : False, "reason" : "File does not exist" }
        return formatResponse(resp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.debug = True
    app.run()
    