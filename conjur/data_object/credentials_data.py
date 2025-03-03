# -*- coding: utf-8 -*-

"""
CredentialsData module

This module represents the DTO that holds credential data
"""

# pylint: disable=too-few-public-methods
class CredentialsData:
    """
    Used for setting user input data to login to Conjur
    """

    def __init__(self, machine=None, login=None, password=None):
        self.machine = machine
        self.login = login
        self.password = password

    @classmethod
    def convert_dict_to_obj(cls, dic):
        """
        Method to convert dictionary to object
        """
        return CredentialsData(**dic)

    # pylint: disable=line-too-long
    def __repr__(self):
        return f"{{'machine': '{self.machine}', 'login': '{self.login}', 'password': '****'}}"

    def __eq__(self, other):
        """
        Method for comparing resources by their values and not by reference
        """
        return self.machine == other.machine and self.login == other.login and self.password == other.password
