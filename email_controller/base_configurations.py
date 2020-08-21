""" Handle all configurations for repository """
from utils_package.api_controller.configman import ConfigmanController

VARS = ConfigmanController().get_application_configs('email_controller', 'vars')
DIRS = ConfigmanController().get_application_configs('email_controller', 'dirs')


class BaseConfigurations:
    """ Handle all configurations for repository """

    @staticmethod
    def smtp_configs():
        """
        Get configs for SMTP controller
        :return:
        """
        smtp_dict = {
            'name': VARS['smtp.server.name'],
            'port': VARS['smtp.server.port'],
            'login_dict': {
                'user': VARS['smtp.server.user'],
                'pass': VARS['smtp.server.pass']
            }
        }
        return smtp_dict

    @staticmethod
    def get_default_values():
        """
        Method to get all application configs and return them
        :return: Both vars and dirs for application
        """
        return VARS, DIRS
