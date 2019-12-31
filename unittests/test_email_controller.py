""" Unit tests for the email controller application
> TODO Add tests for rules violations
"""
import random
from unittest import TestCase
from controller.contact_handler import ContactHandler
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
