from decimal import Decimal
from src.train import Train
from src.types import CoachType, TicketType


class TicketPriceCalculator:
    """Calculator for ticket prices across multiple trains."""

    def __init__(self, trains: list[Train]):
        self.trains = {train.train_number: train for train in trains}

    def calculate(
        self,
        train_number: str,
        number_of_passengers: int,
        from_station: str,
        to_station: str,
        coach_type: CoachType,
        ticket_type: TicketType = TicketType.GENERAL,
    ) -> Decimal:

        # Train not found
        if train_number not in self.trains:
            raise ValueError(f"Train not found: {train_number}")

        train = self.trains[train_number]

        return train.calculate_ticket_price(
            ticket_type=ticket_type,
            coach_type=coach_type,
            number_of_passengers=number_of_passengers,
            from_station=from_station,
            to_station=to_station,
        )
