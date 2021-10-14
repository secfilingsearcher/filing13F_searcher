"""This file contains Exception Classes"""


class NoUrlException(Exception):
    """Raised when the url can't be found"""


class NoAccessionNumberException(Exception):
    """Raised when there is no accession no"""


class InvalidConnectionStringException(Exception):
    """Raised when Connection String Invalid"""


class BadWebPageResponseException(Exception):
    """Raised when Web Page returns no response"""

    def __init__(self, status_code):
        self.status_code = status_code
        super().__init__()


class InvalidUrlException(Exception):
    """Raised when URL is Invalid"""

    def __init__(self, status_code):
        self.status_code = status_code
        super().__init__(excen)
