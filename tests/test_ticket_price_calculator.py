"""Unit tests for TicketPriceCalculator class."""

from decimal import Decimal

import pytest

from src.pricing_strategies import DistanceBasedPricingStrategy, FixPricingStrategy
from src.ticket_price_calculator import TicketPriceCalculator
from src.train import Train
from src.types import CoachType, TicketType


class TestTicketPriceCalculator:
    """Test cases for TicketPriceCalculator class."""

    def test_calculator_initialization_train1_in_trains_dict(self):
        """
        Test TicketPriceCalculator initialization - verify train1 is in trains dict.
        Creates calculator with 2 trains and checks train "1234" is registered.
        """
        strategy = FixPricingStrategy()
        train1 = Train("1234", ["A", "B", "C"], strategy)
        train2 = Train("5678", ["X", "Y", "Z"], strategy)

        calculator = TicketPriceCalculator([train1, train2])

        assert "1234" in calculator.trains

    def test_calculator_initialization_train2_in_trains_dict(self):
        """
        Test TicketPriceCalculator initialization - verify train2 is in trains dict.
        Creates calculator with 2 trains and checks train "5678" is registered.
        """
        strategy = FixPricingStrategy()
        train1 = Train("1234", ["A", "B", "C"], strategy)
        train2 = Train("5678", ["X", "Y", "Z"], strategy)

        calculator = TicketPriceCalculator([train1, train2])

        assert "5678" in calculator.trains

    def test_calculator_initialization_train1_object_stored_correctly(self):
        """
        Test TicketPriceCalculator initialization - verify train1 object is stored.
        Creates calculator and checks that train "1234" maps to correct Train object.
        """
        strategy = FixPricingStrategy()
        train1 = Train("1234", ["A", "B", "C"], strategy)
        train2 = Train("5678", ["X", "Y", "Z"], strategy)

        calculator = TicketPriceCalculator([train1, train2])

        assert calculator.trains["1234"] == train1

    def test_calculator_initialization_train2_object_stored_correctly(self):
        """
        Test TicketPriceCalculator initialization - verify train2 object is stored.
        Creates calculator and checks that train "5678" maps to correct Train object.
        """
        strategy = FixPricingStrategy()
        train1 = Train("1234", ["A", "B", "C"], strategy)
        train2 = Train("5678", ["X", "Y", "Z"], strategy)

        calculator = TicketPriceCalculator([train1, train2])

        assert calculator.trains["5678"] == train2

    def test_calculate_basic(self):
        """Test basic price calculation."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Sawai Madhopur", "Jaipur"]
        train = Train("1234", stations, strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=2,
            from_station="Kota",
            to_station="Jaipur",
            coach_type=CoachType.AC_3,
            ticket_type=TicketType.GENERAL,
        )

        # 2 stations * 50 rs * 2 passengers = 200
        assert price == Decimal("200")

    def test_calculate_default_ticket_type(self):
        """Test calculation with default ticket type (General)."""
        strategy = FixPricingStrategy()
        stations = ["A", "B", "C"]
        train = Train("1234", stations, strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            coach_type=CoachType.SLEEPER,
        )

        # 2 stations * 30 rs * 1 passenger = 60
        assert price == Decimal("60")
