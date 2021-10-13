"""This file contains Exception Classes"""


class NoUrlErrorException(Exception):
    """Raised when the url can't be found"""


class NoAccessionNoException(Exception):
    """Raised when there is no accession no"""


class InvalidConnectionStringException(Exception):
    """Raised when Connection String Invalid"""


class BadWebPageResponseException(Exception):
    """Raised when Web Page returns no response"""


class InvalidUrlException(Exception):
    """Raised when URL is Invalid"""
