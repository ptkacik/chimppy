

class MailChimpException(Exception):
    """Raise this exception if mailchimp return error JSON response.
    Example Error Resopnse JSON
        {
            "status": "error",
            "code": -99,
            "name": "Unknown_Exception",
            "error": "An unknown error occurred processing your request.  Please try again later."
        }
    """
    def __init__(self, code, name, error):
        self.code = code
        self.error = error
        self.name = name

    def __str__(self):
        return 'MailChimp error code: %s, name: %s, error: "%s"' % (
            self.code, self.name, self.error
        )


class NoDeserializerFound(Exception):
    """Raise if deserializion is not Implemented
    """
    pass


class OutputFormatIsNotSupported(Exception):
    """Raise if format is not supported by MailChimp
    """
    pass
