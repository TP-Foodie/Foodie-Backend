import calendar
from datetime import datetime
from models.order import Order
from mongoengine import Q
from services.exceptions.order_exceptions import NonExistingOrderException


def list_all():
    return Order.objects


def get_order(order_id):
    return Order.objects.get(id=order_id)


def get_favor_orders():
    return Order.objects.filter(type=Order.FAVOR_TYPE)


def count():
    return Order.objects.count()


def create(order_type, owner, product, number):
    return Order.objects.create(type=order_type, owner=owner, product=product, number=number)


def update(order_id, field, value):
    order = Order.objects.filter(id=order_id).first()

    if not order:
        raise NonExistingOrderException()

    order[field] = value
    order.save()
    return order


def for_delivery(user_id):
    return Order.objects.filter(delivery=user_id)


def today_count(orders):
    return orders.filter(date=datetime.today()).count()


def month_count(orders):
    today = datetime.today().date()

    first_day, last_day = calendar.monthrange(today.year, today.month)

    begin_month = datetime(today.year, today.month, first_day).date()
    end_month = datetime(today.year, today.month, last_day).date()

    return orders.filter(Q(date__gte=begin_month) & Q(date__lte=end_month)).count()
