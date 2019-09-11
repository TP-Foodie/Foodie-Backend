""" This Module contains all the exceptions that can be thrown in deliveries
disponibles endpoint."""

class DeliveryYaDisponibleException(Exception):
    """ This Class represents exception: delivery ya disponible en la db """
    def __init__(self, message):
        super(DeliveryYaDisponibleException, self).__init__(message)
        self.msg = message

class DeliveryNoDisponibleException(Exception):
    """ This Class represents exception: delivery no disponible en la db """
    def __init__(self, message):
        super(DeliveryNoDisponibleException, self).__init__(message)
        self.msg = message

class ValidationException(Exception):
    """ This Class represents exception: error de validacion en los datos recibidos
    a traves de la api """
    def __init__(self, message):
        super(ValidationException, self).__init__(message)
        self.msg = message
