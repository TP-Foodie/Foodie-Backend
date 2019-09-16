""" This module is the Marshmallow Schema for DeleteAvailableDelivery """

from marshmallow import Schema, fields, validate, post_load

from models.delete_available_delivery import DeleteAvailableDelivery

class DeleteAvailableDeliverySchema(Schema):
    """ This class is the Marshmallow Schema for DeleteAvailableDelivery """
    _id = fields.Str(required=True, validate=validate.Length(min=1))

    class Meta:
        """ Clase que pide Marshmallow para que el schema sea estricto """
        strict = True

    @post_load
    def make_delete_available_delivery(self, data, **kwargs):
        """ This method tells load() return DeleteAvailableDelivery """
        return DeleteAvailableDelivery(**data)
