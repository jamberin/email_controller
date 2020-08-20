""" Unit tests for handling the retrieval of configurations """
from base_configurations import BaseConfigurations
from unittest import TestCase


class TestConfigurations(TestCase):
    """ Tests for handling configurations """

    def setUp(self):
        """ Set up class variables """
        self.base_configs = BaseConfigurations()

    def test_initialization(self):
        """ Confirm that both vars and dirs is returned as expected """
        self.assertIsNotNone(self.base_configs.vars)
        self.assertIsNone(self.base_configs.dirs)
