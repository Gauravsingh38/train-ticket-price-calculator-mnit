"""Unit tests for Train class."""

from decimal import Decimal

import pytest

from src.pricing_strategies import DistanceBasedPricingStrategy, FixPricingStrategy
from src.train import Train
from src.types import CoachType, TicketType


class TestTrain:
    """Test cases for Train class."""

    def test_train_initialization_train_number(self):
        """
        Test Train initialization - verify train_number is set correctly.
        Creates a train with number "1234" and verifies it's stored properly.
        """
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Jaipur"]
        train = Train("1234", stations, strategy)

        assert train.train_number == "1234"

    def test_train_initialization_stations(self):
        """
        Test Train initialization - verify stations list is set correctly.
        Creates a train with 4 stations and verifies the list is stored properly.
        """
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Jaipur"]
        train = Train("1234", stations, strategy)

        assert train.stations == stations

    def test_train_initialization_pricing_strategy(self):
        """
        Test Train initialization - verify pricing_strategy is set correctly.
        Creates a train with FixPricingStrategy and verifies it's stored properly.
        """
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Jaipur"]
        train = Train("1234", stations, strategy)

        assert train.pricing_strategy == strategy

    def test_train_calculate_ticket_price_general(self):
        """Test train ticket price calculation with General ticket."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Sawai Madhopur", "Jaipur"]
        train = Train("1234", stations, strategy)

        price = train.calculate_ticket_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=2,
            from_station="Kota",
            to_station="Jaipur",
        )

        # 2 stations * 50 rs * 2 passengers = 200
        assert price == Decimal("200")

    def test_train_calculate_ticket_price_tatkal(self):
        """Test train ticket price calculation with Tatkal ticket."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Jaipur"]
        train = Train("5678", stations, strategy)

        price = train.calculate_ticket_price(
            ticket_type=TicketType.TATKAL,
            coach_type=CoachType.SLEEPER,
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Jaipur",
        )

        # 3 stations * 50 rs * 1 passenger = 150
        assert price == Decimal("150")

    def test_train_with_distance_based_strategy(self):
        """
        Test train with distance-based pricing strategy.
        Route: A (0km) -> B (100km) -> C (150km).
        Travel: A to B (100km), 1 passenger, Sleeper General.
        Expected: 100 km × ₹1.0 (base) × 1.0 (Sleeper) × 1.0 (General) = ₹100
        """
        station_distances = [
            ("A", Decimal("0")),
            ("B", Decimal("100")),
            ("C", Decimal("150")),
        ]
        strategy = DistanceBasedPricingStrategy(station_distances)
        stations = ["A", "B", "C"]
        train = Train("9999", stations, strategy)

        price = train.calculate_ticket_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.SLEEPER,
            number_of_passengers=1,
            from_station="A",
            to_station="B",
        )

        assert price == Decimal("100")

    def test_train_invalid_station(self):
        """Test error when station is not in train's route."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota"]
        train = Train("1234", stations, strategy)

        with pytest.raises(ValueError, match="Station not found in route"):
            train.calculate_ticket_price(
                ticket_type=TicketType.GENERAL,
                coach_type=CoachType.AC_3,
                number_of_passengers=1,
                from_station="Delhi",
                to_station="Kota",
            )

    def test_train_ac3_coach_type_pricing(self):
        """
        Test train pricing with 3AC coach type.
        Route: A to C (2 stations), 1 passenger, 3AC General.
        Expected: 2 stations × ₹50 (3AC) = ₹100
        """
        strategy = FixPricingStrategy()
        stations = ["A", "B", "C"]
        train = Train("1111", stations, strategy)

        price = train.calculate_ticket_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="A",
            to_station="C",
        )
        assert price == Decimal("100")

    def test_train_sleeper_coach_type_pricing(self):
        """
        Test train pricing with Sleeper coach type.
        Route: A to C (2 stations), 1 passenger, Sleeper General.
        Expected: 2 stations × ₹30 (Sleeper) = ₹60
        """
        strategy = FixPricingStrategy()
        stations = ["A", "B", "C"]
        train = Train("1111", stations, strategy)

        price = train.calculate_ticket_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.SLEEPER,
            number_of_passengers=1,
            from_station="A",
            to_station="C",
        )
        assert price == Decimal("60")

    def test_train_ac2_coach_type_pricing(self):
        """
        Test train pricing with 2AC coach type.
        Route: A to C (2 stations), 1 passenger, 2AC General.
        Expected: 2 stations × ₹70 (2AC) = ₹140
        """
        strategy = FixPricingStrategy()
        stations = ["A", "B", "C"]
        train = Train("1111", stations, strategy)

        price = train.calculate_ticket_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_2,
            number_of_passengers=1,
            from_station="A",
            to_station="C",
        )
        assert price == Decimal("140")

    def test_train_long_route(self):
        """Test train with a long route."""
        strategy = FixPricingStrategy()
        stations = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]
        train = Train("2222", stations, strategy)

        price = train.calculate_ticket_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.SLEEPER,
            number_of_passengers=1,
            from_station="S1",
            to_station="S10",
        )

        # 9 stations * 30 rs * 1 passenger = 270
        assert price == Decimal("270")

    def test_train_adjacent_stations(self):
        """Test train between adjacent stations."""
        strategy = FixPricingStrategy()
        stations = ["A", "B", "C", "D"]
        train = Train("3333", stations, strategy)

        price = train.calculate_ticket_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="B",
            to_station="C",
        )

        # 1 station * 50 rs * 1 passenger = 50
        assert price == Decimal("50")

#sample commit
