""" Validation that a certain email address hasn't violated usage rules
Rules:
0. Less than 3 contacts within the past day
1. Less than 5 contacts within the past week
2. Less than 20 contacts within the past month
3. Less than 40 contacts within the past year
"""
from utils_package.data_controller.scripts.email_controller.email_audit_queries import AuditReader
from utils_package.data_controller.scripts.email_controller.contact_violations_queries import ViolationsWriter
from utils_package.py_utils.logger import logger


class RecordValidation(object):

    def __init__(self):
        """ Initialize Class Variables """
        # Queries
        self.audit_reader = AuditReader()
        self.violations_writer = ViolationsWriter()

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

        # Violation dict for tracking violations
        violation_dict = {
            'strViolationType': None,
            'strViolationAddress': contact_email
        }

        # Collect all contact counts
        day_contact = self.audit_reader.get_record_for_email_within_past_days(contact_email, 0)
        logger.info('Day Count: %s' % str(day_contact))
        week_contact = self.audit_reader.get_record_for_email_within_past_days(contact_email, 6)
        logger.info('Week Count: %s' % str(week_contact))
        month_contact = self.audit_reader.get_record_for_email_within_past_days(contact_email, 29)
        logger.info('Month Count: %s' % str(month_contact))
        year_contact = self.audit_reader.get_record_for_email_within_past_days(contact_email, 364)
        logger.info('Year Count: %s' % str(year_contact))

        # Verify all contact counts
        if day_contact[0] >= 3:
            response['validation'] = True
            response['val_reason'].append('DAY')
            violation_dict['strViolationType'] = 'DAY'
            logger.warning('Rule violation: Daily Contact limit reacheacd: %s' % contact_email)
        if week_contact[0] >= 5:
            response['validation'] = True
            response['val_reason'].append('WEEK')
            violation_dict['strViolationType'] = 'WEEK'
            logger.warning('Rule violation: Weekly Contact limit reacheacd: %s' % contact_email)
        if month_contact[0] >= 20:
            response['validation'] = True
            response['val_reason'].append('MONTH')
            violation_dict['strViolationType'] = 'MONTH'
            logger.warning('Rule violation: Monthly Contact limit reacheacd: %s' % contact_email)
        if year_contact[0] >= 40:
            response['validation'] = True
            response['val_reason'].append('ANNUAL')
            violation_dict['strViolationType'] = 'ANNUAL'
            logger.warning('Rule violation: Yearly Contact limit reacheacd: %s' % contact_email)

        # Write validation error if applicable
        if response['validation']:
            assert violation_dict['strViolationType'] is not None
            self.violations_writer.insert_new_record(violation_dict)

        # TODO BUILD QUEUE TO HANDLE RESPONSES TO USERS
        # Include logic to send an email to the user denoting response
        # Find way to handle contact violation management, perhaps IP blocking
        # For now, just generate way to send canned response for good responses only

        return response
