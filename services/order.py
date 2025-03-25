from typing import Optional, List
from django.db import transaction
from db.models import Order, Ticket, MovieSession, User


def create_order(
    tickets: List[dict],
    username: str,
    date: Optional[str] = None
) -> Order:
    user, _ = User.objects.get_or_create(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        ticket_objects = [
            Ticket(
                movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            for ticket in tickets
        ]
        Ticket.objects.bulk_create(ticket_objects)

    return order

def get_orders(username: Optional[str] = None):
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders