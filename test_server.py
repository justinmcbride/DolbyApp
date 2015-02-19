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
    assert rv.json['error'] == False
    assert rv.json['data']['created'] == True
    assert rv.json['data']['filename'] == 'testFile.json'
