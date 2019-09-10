from marshmallow import Schema, fields, validate, post_load

from deliveries_disponibles.models.eliminar_delivery_disponible import EliminarDeliveryDisponible

class EliminarDeliveryDisponibleSchema(Schema):
    _id = fields.Str(required=True, validate=validate.Length(min=1))

    class Meta:
        strict = True

    @post_load
    def make_eliminar_delivery_disponible(self, data, **kwargs):
        return EliminarDeliveryDisponible(**data)