class DeliveryYaDisponibleException(Exception):
    def __init__(self, message):
        self.msg = message

class DeliveryNoDisponibleException(Exception):
    def __init__(self, message):
        self.msg = message

class ValidationException(Exception):
    def __init__(self, message):
        self.msg = message