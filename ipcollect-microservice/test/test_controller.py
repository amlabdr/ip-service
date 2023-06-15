import unittest
from unittest.mock import patch
import jwt
import time
from requests.models import Response

from controller.controller import ControllerService
from config.config import Config

class TestController(unittest.TestCase):
    @patch('requests.post')
    def test_login(self, mock_post):
        # Create a test JWT token with a payload
        token_payload = {'sub': '1234567890', 'name': 'John Doe', 'iat': time.time(), 'exp': time.time() + 3600}
        test_token = jwt.encode(token_payload, 'secret', algorithm='HS256') 

        # Create a mock response from the post request
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = f'{{"token": "{test_token}"}}'.encode()

        # Configure the mock to return the mock response
        mock_post.return_value = mock_response
    
        config = Config()
        # Create an instance of controllerService and call login
        ctrl_service = ControllerService(config)
        ctrl_service.login()

        # Check that the post request was made with the correct data
        mock_post.assert_called_once_with(ctrl_service.controller_rest_url +'/api/login/user', json={'username': 'admin', 'password': 'admin'})

        # Check that the token was correctly set in the AuthService instance
        self.assertEqual(ctrl_service.token, test_token)

        # Check that the token acquired time was correctly set in the AuthService instance
        decoded_token = jwt.decode(test_token, options={'verify_signature': False})
        self.assertEqual(ctrl_service.token_acquired_time, decoded_token.get('iat'))


if __name__ == '__main__':
    unittest.main()
