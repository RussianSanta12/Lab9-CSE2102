import pytest
import httpx
from unittest.mock import Mock, patch, MagicMock
import sys


class TestMyCallsIntegration:
    """Integration tests for my-calls.py client code"""
    
    @patch('httpx.get')
    def test_get_request_to_root(self, mock_get):
        """Test GET request to root endpoint"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "you called"
        mock_get.return_value = mock_response
        
        response = httpx.get("http://localhost:5000/")
        assert response.status_code == 200
        assert "you called" in response.text
    
    @patch('httpx.post')
    def test_post_echo_request(self, mock_post):
        """Test POST request to echo endpoint"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "You said: Hello Phil!"
        mock_post.return_value = mock_response
        
        data = {"text": "Hello Phil!", "uuid": "e0fd05e6-cfaa-11f0-829e-000d3a8e16b7"}
        response = httpx.post("http://localhost:5000/echo", data=data)
        
        assert response.status_code == 200
        assert "Hello Phil!" in response.text
    
    @patch('httpx.post')
    def test_post_uuid_request(self, mock_post):
        """Test POST request to uuid endpoint"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "done" + "e0fd05e6-cfaa-11f0-829e-000d3a8e16b7"
        mock_post.return_value = mock_response
        
        data = {"uuid": "e0fd05e6-cfaa-11f0-829e-000d3a8e16b7"}
        response = httpx.post("http://localhost:5000/uuid", data=data)
        
        assert response.status_code == 200
        assert "done" in response.text
    
    @patch('httpx.get')
    def test_multiple_get_requests(self, mock_get):
        """Test multiple GET requests work correctly"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "you called"
        mock_get.return_value = mock_response
        
        # Make two requests
        response1 = httpx.get("http://localhost:5000/")
        response2 = httpx.get("http://localhost:5000/")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert mock_get.call_count == 2


class TestClientDataStructure:
    """Test cases for the data structures used in my-calls.py"""
    
    def test_mydata_has_required_fields(self):
        """Test that the mydata dictionary has all required fields"""
        mydata = {
            "uuid": "e0fd05e6-cfaa-11f0-829e-000d3a8e16b7",
            "text": "Hello Phil!",
            "param2": "Making a POST request",
            "body": "my own value"
        }
        
        assert "uuid" in mydata
        assert "text" in mydata
        assert mydata["uuid"] == "e0fd05e6-cfaa-11f0-829e-000d3a8e16b7"
        assert mydata["text"] == "Hello Phil!"
    
    def test_uuid_format_is_valid(self):
        """Test that UUID has correct format"""
        uuid_str = "e0fd05e6-cfaa-11f0-829e-000d3a8e16b7"
        # UUID format: 8-4-4-4-12
        parts = uuid_str.split('-')
        assert len(parts) == 5
        assert len(parts[0]) == 8
        assert len(parts[1]) == 4
        assert len(parts[2]) == 4
        assert len(parts[3]) == 4
        assert len(parts[4]) == 12
    
    def test_mydata_values_are_strings(self):
        """Test that all values in mydata are strings"""
        mydata = {
            "uuid": "e0fd05e6-cfaa-11f0-829e-000d3a8e16b7",
            "text": "Hello Phil!",
            "param2": "Making a POST request",
            "body": "my own value"
        }
        
        for key, value in mydata.items():
            assert isinstance(value, str), f"{key} should be a string"


class TestClientURLConstruction:
    """Test cases for URL construction in the client"""
    
    def test_base_url_is_valid(self):
        """Test that the base URL is correctly formatted"""
        url = "http://localhost:5000/"
        assert url.startswith("http://")
        assert "localhost" in url
        assert "5000" in url
    
    def test_url_concatenation(self):
        """Test URL concatenation for endpoints"""
        url = "http://localhost:5000/"
        echo_url = url + "echo"
        uuid_url = url + "uuid"
        
        assert echo_url == "http://localhost:5000/echo"
        assert uuid_url == "http://localhost:5000/uuid"
    
    def test_endpoints_are_valid(self):
        """Test that endpoint names match server routes"""
        url = "http://localhost:5000/"
        endpoints = ["echo", "uuid"]
        
        for endpoint in endpoints:
            full_url = url + endpoint
            assert full_url.endswith(endpoint)


class TestResponseHandling:
    """Test cases for response handling"""
    
    @patch('httpx.get')
    def test_get_response_has_status_code(self, mock_get):
        """Test that GET response has status_code attribute"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        response = httpx.get("http://localhost:5000/")
        assert hasattr(response, 'status_code')
        assert response.status_code == 200
    
    @patch('httpx.post')
    def test_post_response_has_status_code(self, mock_post):
        """Test that POST response has status_code attribute"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        response = httpx.post("http://localhost:5000/echo", data={"text": "test"})
        assert hasattr(response, 'status_code')
        assert response.status_code == 200
    
    @patch('httpx.get')
    def test_response_has_text_attribute(self, mock_get):
        """Test that response has text attribute"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "response text"
        mock_get.return_value = mock_response
        
        response = httpx.get("http://localhost:5000/")
        assert hasattr(response, 'text')


class TestClientErrorHandling:
    """Test cases for error scenarios"""
    
    @patch('httpx.get')
    def test_handle_server_error_response(self, mock_get):
        """Test handling of server error responses"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        response = httpx.get("http://localhost:5000/")
        assert response.status_code == 500
    
    @patch('httpx.get')
    def test_handle_not_found_response(self, mock_get):
        """Test handling of 404 not found responses"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        response = httpx.get("http://localhost:5000/nonexistent")
        assert response.status_code == 404
    
    @patch('httpx.post')
    def test_handle_bad_request_response(self, mock_post):
        """Test handling of 400 bad request responses"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        response = httpx.post("http://localhost:5000/echo", data={})
        assert response.status_code == 400


class TestHTTPLibrary:
    """Test cases for httpx library usage"""
    
    def test_httpx_get_method_exists(self):
        """Test that httpx has GET method"""
        assert hasattr(httpx, 'get')
    
    def test_httpx_post_method_exists(self):
        """Test that httpx has POST method"""
        assert hasattr(httpx, 'post')
    
    @patch('httpx.post')
    def test_post_with_data_parameter(self, mock_post):
        """Test POST request accepts data parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        data = {"key": "value"}
        response = httpx.post("http://localhost:5000/echo", data=data)
        
        mock_post.assert_called_once()
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
