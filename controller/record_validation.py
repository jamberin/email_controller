""" Validation that a certain email address hasn't violated usage rules
Rules:
0. Less than 3 contacts within the past day
1. Less than 5 contacts within the past week
2. Less than 20 contacts within the past month
3. Less than 40 contacts within the past year
"""
from utils_package.data_controller.scripts.email_controller.email_audit_queries import AuditReader
from utils_package.py_utils.logger import logger


class RecordValidation(object):

    def __init__(self):
        """ Initialize Class Variables """
        # Queries
        self.audit_reader = AuditReader()

    def validate_rule_for_contact(self, contact_email):
        """
        Verify that the email is eligible for another email to be sent
        :param contact_email: String of the email address
        :return: Dict response [boolean check, list rule broken (if applicable)]
        """
        # Build response dictionary
        response = {
            'validation': False,
            'val_reason': []
        }

        # Collect all contact counts
        day_contact = self.audit_reader.get_record_for_email_within_past_days(contact_email, 1)
        week_contact = self.audit_reader.get_record_for_email_within_past_days(contact_email, 7)
        month_contact = self.audit_reader.get_record_for_email_within_past_days(contact_email, 30)
        year_contact = self.audit_reader.get_record_for_email_within_past_days(contact_email, 365)

        # Verify all contact counts
        if day_contact[0] >= 3:
            response['validation'] = True
            response['val_reason'].append('DAY')
            logger.warning('Rule violation: Daily Contact limit reacheacd: %s' % contact_email)
        if week_contact[0] >= 5:
            response['validation'] = True
            response['val_reason'].append('WEEK')
            logger.warning('Rule violation: Weekly Contact limit reacheacd: %s' % contact_email)
        if month_contact[0] >= 20:
            response['validation'] = True
            response['val_reason'].append('MONTH')
            logger.warning('Rule violation: Monthly Contact limit reacheacd: %s' % contact_email)
        if year_contact[0] >= 40:
            response['validation'] = True
            response['val_reason'].append('ANNUAL')
            logger.warning('Rule violation: Yearly Contact limit reacheacd: %s' % contact_email)

        # TODO BUILD QUEUE TO HANDLE RESPONSES TO USERS
        # Include logic to send an email to the user denoting response
        # Find way to handle contact violation management, perhaps IP blocking

        return response
