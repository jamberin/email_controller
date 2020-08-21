""" Handler to respond to and log after a user's contact
> Sends a response email to a user
"""
from email_controller.smtp_controller import GMailController, get_html_template
from email_controller.base_configurations import BaseConfigurations


class ResponseHandler(object):
    """ Handles responses to users """

    def __init__(self):
        """ Initialize class variables """
        self.smtp_config = BaseConfigurations().smtp_configs()
        self.gmail = GMailController(self.smtp_config['login_dict'], self.smtp_config['name'], self.smtp_config['port'])

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
