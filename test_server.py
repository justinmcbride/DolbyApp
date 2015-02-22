import json

def test_listAll(client):
    rv = client.get('/')
    assert rv.json['error'] == False
    assert 'allFiles' in rv.json['data']

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
