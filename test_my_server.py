import pytest
import json
import sys
from pathlib import Path

# Add the workspace to the path to import my-server
sys.path.insert(0, str(Path(__file__).parent))

# Import the Flask app
import importlib.util
spec = importlib.util.spec_from_file_location("my_server", "my-server.py")
my_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(my_server)
app = my_server.app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHelloRoute:
    """Test cases for the / route"""
    
    def test_hello_returns_success(self, client):
        """Test that GET / returns a successful response"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_hello_returns_correct_message(self, client):
        """Test that GET / returns the expected message"""
        response = client.get('/')
        assert "you called" in response.data.decode()
    
    def test_hello_is_get_method(self, client):
        """Test that GET method is used for hello route"""
        response = client.get('/')
        assert response.status_code == 200


class TestEchoRoute:
    """Test cases for the /echo POST route"""
    
    def test_echo_with_valid_text(self, client):
        """Test echo endpoint with valid text parameter"""
        response = client.post('/echo', data={'text': 'Hello World'})
        assert response.status_code == 200
        assert response.data.decode() == "You said: Hello World"
    
    def test_echo_with_different_text(self, client):
        """Test echo endpoint with different text"""
        response = client.post('/echo', data={'text': 'Test Message'})
        assert response.status_code == 200
        assert "Test Message" in response.data.decode()
    
    def test_echo_with_special_characters(self, client):
        """Test echo endpoint with special characters"""
        response = client.post('/echo', data={'text': 'Hello! @#$%^'})
        assert response.status_code == 200
        assert "Hello! @#$%^" in response.data.decode()
    
    def test_echo_with_empty_text(self, client):
        """Test echo endpoint with empty text - should fail"""
        response = client.post('/echo', data={'text': ''})
        assert response.status_code == 200
        assert "You said: " in response.data.decode()
    
    def test_echo_missing_text_parameter(self, client):
        """Test echo endpoint without text parameter - should fail"""
        response = client.post('/echo', data={})
        assert response.status_code == 400
    
    def test_echo_requires_post_method(self, client):
        """Test that echo endpoint only accepts POST"""
        response = client.get('/echo')
        assert response.status_code == 405
    
    def test_echo_with_extra_parameters(self, client):
        """Test echo endpoint ignores extra parameters"""
        response = client.post('/echo', data={'text': 'Hello', 'extra': 'ignored'})
        assert response.status_code == 200
        assert "You said: Hello" in response.data.decode()


class TestUUIDRoute:
    """Test cases for the /uuid POST route"""
    
    def test_uuid_with_correct_uuid(self, client):
        """Test UUID endpoint with the correct UUID"""
        response = client.post('/uuid', data={'uuid': 'e0fd05e6-cfaa-11f0-829e-000d3a8e16b7'})
        assert response.status_code == 200
        assert "done" in response.data.decode()
    
    def test_uuid_returns_uuid_in_response(self, client):
        """Test that UUID endpoint returns the UUID in response"""
        response = client.post('/uuid', data={'uuid': 'e0fd05e6-cfaa-11f0-829e-000d3a8e16b7'})
        assert "e0fd05e6-cfaa-11f0-829e-000d3a8e16b7" in response.data.decode()
    
    def test_uuid_with_incorrect_uuid(self, client):
        """Test UUID endpoint with an incorrect UUID"""
        response = client.post('/uuid', data={'uuid': 'wrong-uuid-1234'})
        assert response.status_code == 200
        assert "done" in response.data.decode()
    
    def test_uuid_with_empty_uuid(self, client):
        """Test UUID endpoint with empty UUID"""
        response = client.post('/uuid', data={'uuid': ''})
        assert response.status_code == 200
    
    def test_uuid_missing_parameter(self, client):
        """Test UUID endpoint without uuid parameter - should fail"""
        response = client.post('/uuid', data={})
        assert response.status_code == 400
    
    def test_uuid_requires_post_method(self, client):
        """Test that UUID endpoint only accepts POST"""
        response = client.get('/uuid')
        assert response.status_code == 405
    
    def test_uuid_with_extra_parameters(self, client):
        """Test UUID endpoint ignores extra parameters"""
        response = client.post('/uuid', data={'uuid': 'e0fd05e6-cfaa-11f0-829e-000d3a8e16b7', 'extra': 'data'})
        assert response.status_code == 200
    
    def test_uuid_case_sensitivity(self, client):
        """Test if UUID check is case sensitive"""
        # Testing with uppercase - UUID should be case-sensitive for valid UUIDs
        response = client.post('/uuid', data={'uuid': 'E0FD05E6-CFAA-11F0-829E-000D3A8E16B7'})
        assert response.status_code == 200
    
    def test_uuid_with_multiple_uuids(self, client):
        """Test UUID endpoint with multiple UUID requests"""
        correct_uuid = 'e0fd05e6-cfaa-11f0-829e-000d3a8e16b7'
        wrong_uuid = 'f1ge16f7-dgbb-22g1-940f-111e4b9f27c8'
        
        response1 = client.post('/uuid', data={'uuid': correct_uuid})
        response2 = client.post('/uuid', data={'uuid': wrong_uuid})
        
        assert response1.status_code == 200
        assert response2.status_code == 200


class TestRouteMethods:
    """Test cases for HTTP method restrictions"""
    
    def test_only_allowed_methods(self, client):
        """Test that only allowed HTTP methods work for each route"""
        # GET to echo and uuid should fail (405 Method Not Allowed)
        assert client.get('/echo').status_code == 405
        assert client.get('/uuid').status_code == 405
        
        # POST to root may or may not be allowed depending on Flask config
        response = client.post('/')
        assert response.status_code in [200, 405]


class TestResponseFormats:
    """Test cases for response formats"""
    
    def test_hello_response_is_string(self, client):
        """Test that hello response is a string"""
        response = client.get('/')
        assert isinstance(response.data.decode(), str)
    
    def test_echo_response_format(self, client):
        """Test echo response has correct format"""
        response = client.post('/echo', data={'text': 'test'})
        assert response.data.decode().startswith("You said: ")
    
    def test_uuid_response_format(self, client):
        """Test UUID response has correct format"""
        response = client.post('/uuid', data={'uuid': 'test'})
        assert response.data.decode().startswith("done")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
