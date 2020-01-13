""" Handler to respond to and log after a user's contact
> Sends a response email to a user
"""
from email_controller.smtp_controller import GMailController, get_html_template
from utils_package.data_controller.json_config import JSONConfig
from utils_package.py_utils import primary_utils


class ResponseHandler(object):
    """ Handles responses to users """

    def __init__(self):
        """ Initialize class variables """
        self.config = JSONConfig()
        self.gmail = GMailController(self.config.get_smtp_dict('primary_gmail'))
        self.utils = primary_utils

    def send_response_email(self, email_address):
        """
        Sends the email template
        :param email_address:
        :return:
        """
        template = get_html_template('contact_response.html')
        subject = 'beringersolutions.com | Thanks for reaching out!'
        response = self.gmail.attempt_send_message(template, email_address, subject, message_type='html')
        return response
