import pytest
from MainServer import create_app

@pytest.fixture
def app():
    app = create_app(testing=True)
    app.config['TESTING'] = True
    return app