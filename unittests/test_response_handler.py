""" Unit tests for the response handler application """
from email_controller.response_handler import ResponseHandler
from unittest import TestCase


class TestResponseHandler(TestCase):
    """ Unit tests for response handler """

    def setUp(self):
        """ Set up class variables """
        self.response_handler = ResponseHandler()

    def test_send_email(self):
        """ Test to send the standard response email
        1. Set up test data
        2. Send email
        3. Verify response
        """
        # 1. Set up test data
        email_address = 'jamberin@gmail.com'

        # 2. Send email
        response = self.response_handler.send_response_email(email_address)

        # 3. Verify response
        self.assertTrue(response)
