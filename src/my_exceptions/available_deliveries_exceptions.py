""" This Module contains all the exceptions that can be thrown in available deliveries endpoint."""

class DeliveryAlreadyAvailableException(Exception):
    """ This Class represents exception: delivery already available in db. """
    def __init__(self, message):
        super(DeliveryAlreadyAvailableException, self).__init__(message)
        self.msg = message

class DeliveryNotAvailableException(Exception):
    """ This Class represents exception: delivery not available in db. """
    def __init__(self, message):
        super(DeliveryNotAvailableException, self).__init__(message)
        self.msg = message

class ValidationException(Exception):
    """ This Class represents exception: validation error of request data. """
    def __init__(self, message):
        super(ValidationException, self).__init__(message)
        self.msg = message
