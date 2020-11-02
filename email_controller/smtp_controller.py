""" Primary email_controller for SMTP control
> Will handle the default SMTP control to format HTML and send emails
> Configured for gmail only currently
> Updated and confirmed working on server and locally
"""
from smtplib import SMTPDataError, SMTPSenderRefused, SMTPRecipientsRefused, SMTPHeloError, SMTP_SSL
import ssl
import codecs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils_package.py_utils.logger import logger

from email_controller.base_configurations import DIRS


def log_email_payload(login_dict, message, recipient, subject):
    """
    Reusable method to log email payload
    :param login_dict:
    :param message:
    :param recipient:
    :param subject:
    """
    logger.debug('Login Dict: [user: %s, pass: %s]' % (login_dict['user'], login_dict['pass']))
    logger.debug('Message: %s' % str(message))
    logger.debug('Subject: %s' % subject)
    logger.debug('Recipient: %s' % recipient)


def get_html_template(template_name):
    """
    Return the HTML content of the template file
    :param template_name: Location of the file within the email templates directory
    :return: HTML template
    """
    template_dir = DIRS['email.templates.html']
    template_location = template_dir + template_name
    file = codecs.open(template_location, 'r')
    f = file.read()
    file.close()
    return f


class GMailController(object):
    """ Main email_controller for SMTP """

    def __init__(self, login_dict, server, port):
        """
        Initialize class variables
        :param login_dict: login_dict: Dictionary of login credentials [user, pass]
        :param server: SMTP server name
        :param port: Port for SMTP traffic
        """
        self.to_address = login_dict['user']
        self.context = ssl.create_default_context()
        self.login_dict = login_dict
        self.server = server
        self.port = port

    def attempt_send_message(self, message, recipient, subject, message_type='text'):
        """
        Attempts to send the message
        :param
        :param message: HTML message object
        :param recipient: Recipient of the email
        :param subject: Subject line of the email
        :param message_type: Either text or html
        :return: Success or failure messages
        """
        chk = True
        logger.info('Starting email send attempt')
        html_msg = MIMEMultipart('alternative')
        html_msg['Subject'] = subject
        html_msg['To'] = recipient

        if message_type.lower() == 'text':
            message_builder = MIMEText(message, 'plain')
        elif message_type.lower() == 'html':
            message_builder = MIMEText(str(message), 'html')
        else:
            logger.error('Message type not recognized')
            raise Exception('Message type not recognized')

        html_msg.attach(message_builder)

        try:
            email_server = SMTP_SSL(self.server, self.port, context=self.context)
            email_server.login(self.login_dict['user'], self.login_dict['pass'])
            email_server.sendmail(self.to_address, recipient, html_msg.as_string())
        except SMTPDataError or SMTPSenderRefused or SMTPRecipientsRefused or SMTPHeloError:
            logger.error('Issue with sending email')
            chk = False
        logger.info('Successfully sent email')
        return chk
