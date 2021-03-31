"""Custom Exceptions"""


class NoUrlsError(Exception):
    """Exception Raised when there are no URLS

    Attributes:
    message -- explanation of the error
    """

    def __init__(self, message="There are no urls on the page"):
        self.message = message
        super().__init__(self.message)
