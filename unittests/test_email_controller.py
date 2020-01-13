""" Unit tests for the email email_controller application
> TODO Add tests for rules violations
"""
import random
from unittest import TestCase
from email_controller.contact_handler import ContactHandler
from utils_package.data_controller.scripts.email_controller.email_audit_queries import AuditReader


class TestEmailController(TestCase):
    """ Send a sample email """

    def setUp(self):
        """ Set up class variables """
        self.contact = ContactHandler()
        self.audit_reader = AuditReader()

    def test_send_email_no_violation(self):
        """ Send a sample email like what would come from the contact form
        1. Set up test data
        2. Send data to contact form
        3. Confirm contact form record stored
        """
        # 1. Set up test data
        name = 'John Denver'
        email = 'john.denver%s@website.net' % str(random.randint(0000, 9999))
        message = 'Test simple plain text message'

        # 2. Send data to contact form
        status_code, display_message, response = self.contact.contact_form_entry(name, email, message)
        self.assertEqual(201, status_code)
        self.assertEqual('Your message has been sent! I will be in contact shortly.', display_message)
        self.assertIsNotNone(response)

        # 3. Confirm contact form record stored
        response = self.audit_reader.get_all_record_for_email(email)
        self.assertIsNotNone(response)

    def test_violation(self):
        """ Send more than 3 emails in one day
        1. Set up test data
        2. Send data to contact form
        3. Confirm contact form records stored
        4. Validate the error response on the last run
        """
        # 1. Set up test data
        name = 'John Denver'
        email = 'john.denver%s@website.net' % str(random.randint(0000, 9999))
        message = 'Test simple plain text message'

        # 2. Send data to contact form
        r = range(3)
        for _ in r:
            status_code, display_message, response = self.contact.contact_form_entry(name, email, message +
                                                                                     ' %s' % str(_))
            self.assertEqual(201, status_code)
            self.assertEqual('Your message has been sent! I will be in contact shortly.', display_message)
            self.assertIsNotNone(response)

        # 3. Confirm contact form records stored
        response = self.audit_reader.get_all_record_for_email(email)
        self.assertIsNotNone(response)

        # 4. Validate the error response on the last run
        status_code, display_message, response = self.contact.contact_form_entry(name, email, message)
        self.assertEqual(429, status_code)
        self.assertEqual('It looks like you have tried to contact too many times. Over three times in the last day. ',
                         display_message)
        self.assertIsNotNone(response)
