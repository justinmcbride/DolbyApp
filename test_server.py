import json

def test_listAll(client):
    rv = client.get('/')
    assert rv.json['error'] == False
    assert 'allFiles' in rv.json['data']
    assert len(rv.json['data']['allFiles']) == 0

def test_postSingle(client):
    rv = client.post('/file/testFile.json', data=json.dumps({
        'val1' : 10,
        'val2' : "some value",
        'val3' : [ 1, 2, "blah" ]
    }), follow_redirects=True, content_type='application/json')
    assert 'error' in rv.json
    assert rv.json['error'] == False
    assert rv.json['data']['created'] == True
    assert rv.json['data']['filename'] == 'testFile.json'

    rv = client.post('/file/testFile.blah', data=json.dumps({
        'val1' : 10,
        'val2' : "some value",
        'val3' : [ 1, 2, "blah" ]
    }), follow_redirects=True, content_type='application/json')
    assert 'error' in rv.json
    assert rv.json['error'] == True
    assert 'data' in rv.json
    assert rv.json['data'] == "Filename needs to be a .json file"

def test_getSingle(client):
    rv = client.get('/file/testFile.json')
    assert 'error' in rv.json
    assert rv.json['error'] == False
    assert 'data' in rv.json
    assert 'val1' in rv.json['data']
    assert rv.json['data']['val1'] == 10
    assert 'val2' in rv.json['data']
    assert rv.json['data']['val2'] == "some value"
    assert 'val3' in rv.json['data']
    assert rv.json['data']['val3'] == [ 1, 2, "blah" ]
    assert rv.json['data']

def test_putSingle(client):
    rv = client.put('/file/testFile.json', data=json.dumps({
        'val1' : 15,
        'val2' : None,
        'val4' : "new"
    }), follow_redirects=True, content_type='application/json')
    assert 'error' in rv.json
    assert rv.json['error'] == False
    assert 'data' in rv.json

    data = rv.json['data']
    assert 'changes' in data

    assert 'additions' in data['changes']
    assert len(data['changes']['additions']) == 1

    assert 'removals' in data['changes']
    assert len(data['changes']['removals']) == 1

    assert 'modifications' in data['changes']
    assert len(data['changes']['modifications']) == 1

def test_deleteSingle(client):
    rv = client.delete('/file/testFile.json')
    assert 'error' in rv.json
    assert rv.json['error'] == False
    assert 'data' in rv.json
    assert 'deleted' in rv.json['data']
    assert rv.json['data']['deleted'] == True

def test_postMultiple(client):
    rv = client.post('/files', data=json.dumps({
        'file1.json' : {
            'val1' : 10,
            'val2' : "some value",
            'val3' : [ 1, 2, "blah" ]
            },
        'file2.json' : {
            'val1' : 10,
            'val2' : "some value",
            'val3' : [ 1, 2, "blah" ]
        },
        'file3.json' : {
            'val1' : 10,
            'val2' : "some value",
            'val3' : [ 1, 2, "blah" ]
        },
        'file4.blah' : {
            'val1' : 10,
            'val2' : "some value",
            'val3' : [ 1, 2, "blah" ]
        }
    }), follow_redirects=True, content_type='application/json')
    assert 'error' in rv.json
    assert rv.json['error'] == False
    assert 'data' in rv.json

def test_putMultiple(client):
    rv = client.put('/files', data=json.dumps({
        'file1.json' : {
            'val1' : 5,
            'val2' : 2,
            'val3' : None,
            'val4' : 1,
            'val5' : 2
            },
        'file2.json' : {
            'val1' : None
        },
        'file4.blah' : {
            'val1' : 10,
            'val2' : [ 1, 2, "blah" ],
            'val3' : 2
        }
    }), follow_redirects=True, content_type='application/json')
    assert 'error' in rv.json
    assert rv.json['error'] == False
    assert 'data' in rv.json

    data = rv.json['data']
    assert 'file1.json' in data
    assert 'file2.json' in data
    assert 'file4.blah' in data

    assert 'modified' in data['file1.json']
    assert 'modified' in data['file2.json']
    assert 'modified' in data['file4.blah']

    assert data['file1.json']['modified'] == True
    assert data['file2.json']['modified'] == True
    assert data['file4.blah']['modified'] == False

    assert 'information' in data['file1.json']
    assert 'information' in data['file2.json']
    assert 'information' in data['file4.blah']

    assert data['file4.blah']['information'] == "File does not exist; first POST it"

    assert 'changes' in data['file1.json']['information']
    assert 'changes' in data['file2.json']['information']

    assert 'additions' in data['file1.json']['information']['changes']
    assert 'additions' in data['file2.json']['information']['changes']

    assert 'removals' in data['file1.json']['information']['changes']
    assert 'removals' in data['file2.json']['information']['changes']

    assert 'modifications' in data['file1.json']['information']['changes']
    assert 'modifications' in data['file2.json']['information']['changes']

    assert len(data['file1.json']['information']['changes']['additions']) == 2
    assert len(data['file2.json']['information']['changes']['additions']) == 0

    assert len(data['file1.json']['information']['changes']['removals']) == 1
    assert len(data['file2.json']['information']['changes']['removals']) == 1

    assert len(data['file1.json']['information']['changes']['modifications']) == 2
    assert len(data['file2.json']['information']['changes']['modifications']) == 0


def test_deleteMultiple(client):
    rv = client.delete('/files/file1.json+file2.json+file3.json+file4.blah')
    assert 'error' in rv.json
    assert rv.json['error'] == False
    assert 'data' in rv.json
    assert 'file1.json' in rv.json['data']
    assert 'file2.json' in rv.json['data']
    assert 'file3.json' in rv.json['data']
    assert 'file4.blah' in rv.json['data']

    assert 'deleted' in rv.json['data']['file1.json']
    assert 'reason' not in rv.json['data']['file1.json']
    assert rv.json['data']['file1.json']['deleted'] == True

    assert 'deleted' in rv.json['data']['file2.json']
    assert 'reason' not in rv.json['data']['file2.json']
    assert rv.json['data']['file2.json']['deleted'] == True

    assert 'deleted' in rv.json['data']['file3.json']
    assert 'reason' not in rv.json['data']['file3.json']
    assert rv.json['data']['file3.json']['deleted'] == True

    assert 'deleted' in rv.json['data']['file4.blah']
    assert 'reason' in rv.json['data']['file4.blah']
    assert rv.json['data']['file4.blah']['deleted'] == False
    assert rv.json['data']['file4.blah']['reason'] == "File does not exist"
