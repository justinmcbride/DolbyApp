import pytest
from MainServer import create_app

@pytest.fixture
def app():
	return create_app()