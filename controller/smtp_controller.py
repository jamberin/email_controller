""" Primary controller for SMTP control
> Will handlge the default SMTP control to format HTML and send emails
> Configured for gmail only currently
"""
from smtplib import SMTPException, SMTPResponseException, SMTPConnectError, SMTPHeloError, SMTP_SSL
from utils_package.py_utils.logger import logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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


class GMailController(object):
    """ Main controller for SMTP """

    def __init__(self):
        """ Initialize class variables """
        self.server = SMTP_SSL('smtp.gmail.com', 465)

    def attempt_send_message(self, login_dict, message, recipient, subject, message_type='text'):
        """
        Attempts to send the message
        :param login_dict: Dictionary of login credentials [user, pass]
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
            message_builder = MIMEText(message, 'html')
        else:
            logger.error('Message type not recognized')
            raise Exception('Message type not recognized')

        html_msg.attach(message_builder)

        try:
            self.server.ehlo()
            self.server.login(login_dict['user'], login_dict['pass'])
            self.server.sendmail(login_dict['user'], recipient, html_msg.as_string())
            self.server.quit()
            logger.info('Successfully sent email')
        except TypeError:
            logger.error('Email not sent, issues with data types')
            log_email_payload(login_dict, message, recipient, subject)
            chk = False
        except SMTPException or SMTPResponseException:
            logger.error('Email not sent, exception with SMTP')
            log_email_payload(login_dict, message, recipient, subject)
            chk = False
        except SMTPConnectError or SMTPHeloError:
            logger.error('Email not sent, error with SMTP')
            log_email_payload(login_dict, message, recipient, subject)
            chk = False
        finally:
            logger.info('Completed email send attempt')
            return chk
