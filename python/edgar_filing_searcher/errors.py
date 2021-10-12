"""This file contains Exception Classes"""


class NoUrlException(Exception):
    """Raised when the url can't be found"""


class IncorrectUrlException(Exception):
    """Raised when the url can't be found"""


class NoAccessionNo(Exception):
    """Raised when there is no accession no"""


class InvalidConnectionStringException(Exception):
    """Raised when Connection String Invalid"""


class BadSearchPageException(Exception):
    """Raised when Connection String Invalid"""
