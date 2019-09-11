""" This module is the Marshmallow Schema for EliminarDeliveryDisponible """

from marshmallow import Schema, fields, validate, post_load

from deliveries_disponibles.models.eliminar_delivery_disponible import EliminarDeliveryDisponible

class EliminarDeliveryDisponibleSchema(Schema):
    """ This class is the Marshmallow Schema for EliminarDeliveryDisponible """
    _id = fields.Str(required=True, validate=validate.Length(min=1))

    class Meta:
        """ Clase que pide Marshmallow para que el schema sea estricto """
        strict = True

    @post_load
    def make_eliminar_delivery_disponible(self, data, **kwargs):
        """ This method tells load() return EliminarDeliveryDisponible """
        return EliminarDeliveryDisponible(**data)
