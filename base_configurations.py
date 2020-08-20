""" Handle all configurations for repository """
from utils_package.api_controller.configman import ConfigmanController


class BaseConfigurations:
    """ Handle all configurations for repository """

    def __init__(self):
        self.configman = ConfigmanController()
        self.vars = self.configman.get_application_configs('email_controller', 'vars')
        self.dirs = self.configman.get_application_configs('email_controller', 'dirs')
