"""Integration tests for the train ticket price calculator."""

from decimal import Decimal

import pytest

from src.pricing_strategies import DistanceBasedPricingStrategy, FixPricingStrategy
from src.ticket_price_calculator import TicketPriceCalculator
from src.train import Train
from src.types import CoachType, TicketType


class TestIntegration:
    """Integration tests for the complete system."""

    def test_complete_workflow_example_from_requirements(self):
        """
        Test the exact example from requirements:
        Train 1234 from Mumbai to Jaipur
        Stations: Mumbai -> Surat -> Kota -> Sawai Madhopur -> Jaipur
        2 passengers from Kota to Jaipur in 3AC General Ticket
        Expected: 200 rs (2 stations between Kota and Jaipur)
        """
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

        assert price == Decimal("200")

    def test_multiple_trains_train1_mumbai_to_kota_sleeper_general(self):
        """
        Test Train 1234 (Mumbai-Jaipur route) with 1 passenger.
        Route: Mumbai to Kota in Sleeper class, General ticket.
        Expected: 2 stations × ₹30 (Sleeper) × 1 passenger = ₹60
        """
        strategy = FixPricingStrategy()
        train1 = Train(
            "1234", ["Mumbai", "Surat", "Kota", "Sawai Madhopur", "Jaipur"], strategy
        )
        train2 = Train(
            "5678",
            ["Delhi", "Agra", "Bhopal", "Nagpur", "Hyderabad", "Bangalore"],
            strategy,
        )
        train3 = Train(
            "9012",
            ["Kolkata", "Bhubaneswar", "Visakhapatnam", "Vijayawada", "Chennai"],
            strategy,
        )
        calculator = TicketPriceCalculator([train1, train2, train3])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Kota",
            coach_type=CoachType.SLEEPER,
            ticket_type=TicketType.GENERAL,
        )
        assert price == Decimal("60")

    def test_multiple_trains_train2_delhi_to_bangalore_ac2_tatkal_3_passengers(self):
        """
        Test Train 5678 (Delhi-Bangalore route) with 3 passengers.
        Route: Delhi to Bangalore in 2AC class, Tatkal ticket.
        Expected: 5 stations × ₹140 (2AC Tatkal) × 3 passengers = ₹2100
        """
        strategy = FixPricingStrategy()
        train1 = Train(
            "1234", ["Mumbai", "Surat", "Kota", "Sawai Madhopur", "Jaipur"], strategy
        )
        train2 = Train(
            "5678",
            ["Delhi", "Agra", "Bhopal", "Nagpur", "Hyderabad", "Bangalore"],
            strategy,
        )
        train3 = Train(
            "9012",
            ["Kolkata", "Bhubaneswar", "Visakhapatnam", "Vijayawada", "Chennai"],
            strategy,
        )
        calculator = TicketPriceCalculator([train1, train2, train3])

        price = calculator.calculate(
            train_number="5678",
            number_of_passengers=3,
            from_station="Delhi",
            to_station="Bangalore",
            coach_type=CoachType.AC_2,
            ticket_type=TicketType.TATKAL,
        )
        assert price == Decimal("2100")

    def test_multiple_trains_train3_kolkata_to_chennai_ac3_general_2_passengers(self):
        """
        Test Train 9012 (Kolkata-Chennai route) with 2 passengers.
        Route: Kolkata to Chennai in 3AC class, General ticket.
        Expected: 4 stations × ₹50 (3AC General) × 2 passengers = ₹400
        """
        strategy = FixPricingStrategy()
        train1 = Train(
            "1234", ["Mumbai", "Surat", "Kota", "Sawai Madhopur", "Jaipur"], strategy
        )
        train2 = Train(
            "5678",
            ["Delhi", "Agra", "Bhopal", "Nagpur", "Hyderabad", "Bangalore"],
            strategy,
        )
        train3 = Train(
            "9012",
            ["Kolkata", "Bhubaneswar", "Visakhapatnam", "Vijayawada", "Chennai"],
            strategy,
        )
        calculator = TicketPriceCalculator([train1, train2, train3])

        price = calculator.calculate(
            train_number="9012",
            number_of_passengers=2,
            from_station="Kolkata",
            to_station="Chennai",
            coach_type=CoachType.AC_3,
            ticket_type=TicketType.GENERAL,
        )
        assert price == Decimal("400")

    def test_general_ticket_ac3_coach_pricing(self):
        """
        Test General ticket pricing for 3AC coach.
        Route: A to C (2 stations), 1 passenger, 3AC General.
        Expected: 2 stations × ₹50 (3AC General) = ₹100
        """
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C"], strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            coach_type=CoachType.AC_3,
            ticket_type=TicketType.GENERAL,
        )
        assert price == Decimal("100")

    def test_general_ticket_sleeper_coach_pricing(self):
        """
        Test General ticket pricing for Sleeper coach.
        Route: A to C (2 stations), 1 passenger, Sleeper General.
        Expected: 2 stations × ₹30 (Sleeper General) = ₹60
        """
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C"], strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            coach_type=CoachType.SLEEPER,
            ticket_type=TicketType.GENERAL,
        )
        assert price == Decimal("60")

    def test_general_ticket_ac2_coach_pricing(self):
        """
        Test General ticket pricing for 2AC coach.
        Route: A to C (2 stations), 1 passenger, 2AC General.
        Expected: 2 stations × ₹70 (2AC General) = ₹140
        """
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C"], strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            coach_type=CoachType.AC_2,
            ticket_type=TicketType.GENERAL,
        )
        assert price == Decimal("140")

    def test_general_ticket_ac1_coach_pricing(self):
        """
        Test General ticket pricing for 1AC coach.
        Route: A to C (2 stations), 1 passenger, 1AC General.
        Expected: 2 stations × ₹100 (1AC General) = ₹200
        """
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C"], strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            coach_type=CoachType.AC_1,
            ticket_type=TicketType.GENERAL,
        )
        assert price == Decimal("200")

    def test_general_ticket_general_coach_pricing(self):
        """
        Test General ticket pricing for General coach.
        Route: A to C (2 stations), 1 passenger, General class General ticket.
        Expected: 2 stations × ₹20 (General class General) = ₹40
        """
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C"], strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            coach_type=CoachType.GENERAL,
            ticket_type=TicketType.GENERAL,
        )
        assert price == Decimal("40")

    def test_tatkal_ticket_ac3_coach_pricing(self):
        """
        Test Tatkal ticket pricing for 3AC coach.
        Route: A to C (2 stations), 1 passenger, 3AC Tatkal.
        Expected: 2 stations × ₹100 (3AC Tatkal) = ₹200
        """
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C"], strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            coach_type=CoachType.AC_3,
            ticket_type=TicketType.TATKAL,
        )
        assert price == Decimal("200")

    def test_tatkal_ticket_sleeper_coach_pricing(self):
        """
        Test Tatkal ticket pricing for Sleeper coach.
        Route: A to C (2 stations), 1 passenger, Sleeper Tatkal.
        Expected: 2 stations × ₹50 (Sleeper Tatkal) = ₹100
        """
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C"], strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            coach_type=CoachType.SLEEPER,
            ticket_type=TicketType.TATKAL,
        )
        assert price == Decimal("100")

    def test_tatkal_ticket_ac2_coach_pricing(self):
        """
        Test Tatkal ticket pricing for 2AC coach.
        Route: A to C (2 stations), 1 passenger, 2AC Tatkal.
        Expected: 2 stations × ₹140 (2AC Tatkal) = ₹280
        """
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C"], strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            coach_type=CoachType.AC_2,
            ticket_type=TicketType.TATKAL,
        )
        assert price == Decimal("280")

    def test_tatkal_ticket_ac1_coach_pricing(self):
        """
        Test Tatkal ticket pricing for 1AC coach.
        Route: A to C (2 stations), 1 passenger, 1AC Tatkal.
        Expected: 2 stations × ₹200 (1AC Tatkal) = ₹400
        """
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C"], strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            coach_type=CoachType.AC_1,
            ticket_type=TicketType.TATKAL,
        )
        assert price == Decimal("400")

    def test_tatkal_ticket_general_coach_pricing(self):
        """
        Test Tatkal ticket pricing for General coach.
        Route: A to C (2 stations), 1 passenger, General class Tatkal.
        Expected: 2 stations × ₹40 (General class Tatkal) = ₹80
        """
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C"], strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            coach_type=CoachType.GENERAL,
            ticket_type=TicketType.TATKAL,
        )
        assert price == Decimal("80")

    def test_distance_based_pricing_integration(self):
        """
        Test integration with distance-based pricing strategy.
        Route: Mumbai (0km) -> Surat (264km) -> Kota (486km) -> Jaipur (400km).
        Travel: Mumbai to Jaipur (1150km total), 1 passenger, 3AC General.
        Expected: 1150 km × ₹1.0 (base) × 1.5 (3AC) × 1.0 (General) = ₹1725
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("264")),
            ("Kota", Decimal("486")),
            ("Jaipur", Decimal("400")),
        ]

        strategy = DistanceBasedPricingStrategy(station_distances)
        train = Train("1234", ["Mumbai", "Surat", "Kota", "Jaipur"], strategy)
        calculator = TicketPriceCalculator([train])

        # Test Mumbai to Jaipur
        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Jaipur",
            coach_type=CoachType.AC_3,
            ticket_type=TicketType.GENERAL,
        )
        assert price == Decimal("1725")

    def test_mixed_pricing_strategies_fixed_pricing_train(self):
        """
        Test fixed pricing strategy when multiple trains use different strategies.
        Train 1234 uses fixed pricing: A to D (3 stations), Sleeper General.
        Expected: 3 stations × ₹30 (Sleeper General) = ₹90
        """
        fix_strategy = FixPricingStrategy()
        train1 = Train("1234", ["A", "B", "C", "D"], fix_strategy)

        station_distances = [
            ("A", Decimal("0")),
            ("B", Decimal("100")),
            ("C", Decimal("100")),
            ("D", Decimal("100")),
        ]
        distance_strategy = DistanceBasedPricingStrategy(station_distances)
        train2 = Train("5678", ["A", "B", "C", "D"], distance_strategy)

        calculator = TicketPriceCalculator([train1, train2])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="A",
            to_station="D",
            coach_type=CoachType.SLEEPER,
            ticket_type=TicketType.GENERAL,
        )
        assert price == Decimal("90")

    def test_mixed_pricing_strategies_distance_based_train(self):
        """
        Test distance-based pricing when multiple trains use different strategies.
        Train 5678 uses distance-based: A (0km) -> B (100km) -> C (100km) -> D (100km).
        Travel: A to D (300km total), 1 passenger, Sleeper General.
        Expected: 300 km × ₹1.0 (base) × 1.0 (Sleeper) × 1.0 (General) = ₹300
        """
        fix_strategy = FixPricingStrategy()
        train1 = Train("1234", ["A", "B", "C", "D"], fix_strategy)

        station_distances = [
            ("A", Decimal("0")),
            ("B", Decimal("100")),
            ("C", Decimal("100")),
            ("D", Decimal("100")),
        ]
        distance_strategy = DistanceBasedPricingStrategy(station_distances)
        train2 = Train("5678", ["A", "B", "C", "D"], distance_strategy)

        calculator = TicketPriceCalculator([train1, train2])

        price = calculator.calculate(
            train_number="5678",
            number_of_passengers=1,
            from_station="A",
            to_station="D",
            coach_type=CoachType.SLEEPER,
            ticket_type=TicketType.GENERAL,
        )
        assert price == Decimal("300")

    def test_real_world_scenario_family_travel(self):
        """Test real-world scenario: Family of 4 traveling."""
        strategy = FixPricingStrategy()
        train = Train(
            "12345", ["Delhi", "Mathura", "Agra", "Gwalior", "Jhansi", "Bhopal"], strategy
        )
        calculator = TicketPriceCalculator([train])

        # Family of 4 from Delhi to Bhopal in 3AC General
        price = calculator.calculate(
            train_number="12345",
            number_of_passengers=4,
            from_station="Delhi",
            to_station="Bhopal",
            coach_type=CoachType.AC_3,
            ticket_type=TicketType.GENERAL,
        )

        # 5 stations * 50 rs * 4 passengers = 1000
        assert price == Decimal("1000")

    def test_real_world_scenario_last_minute_booking(self):
        """Test real-world scenario: Last minute Tatkal booking."""
        strategy = FixPricingStrategy()
        train = Train("22222", ["Mumbai", "Pune", "Solapur", "Hyderabad"], strategy)
        calculator = TicketPriceCalculator([train])

        # Single passenger, Tatkal ticket, 2AC
        price = calculator.calculate(
            train_number="22222",
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Hyderabad",
            coach_type=CoachType.AC_2,
            ticket_type=TicketType.TATKAL,
        )

        # 3 stations * 140 rs * 1 passenger = 420
        assert price == Decimal("420")

    def test_real_world_scenario_budget_travel(self):
        """Test real-world scenario: Budget travel in general coach."""
        strategy = FixPricingStrategy()
        train = Train(
            "33333", ["Kolkata", "Asansol", "Dhanbad", "Gaya", "Patna"], strategy
        )
        calculator = TicketPriceCalculator([train])

        # 2 passengers in General coach
        price = calculator.calculate(
            train_number="33333",
            number_of_passengers=2,
            from_station="Kolkata",
            to_station="Patna",
            coach_type=CoachType.GENERAL,
            ticket_type=TicketType.GENERAL,
        )

        # 4 stations * 20 rs * 2 passengers = 160
        assert price == Decimal("160")

    def test_edge_case_adjacent_stations(self):
        """Test edge case: Travel between adjacent stations."""
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C", "D", "E"], strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="B",
            to_station="C",
            coach_type=CoachType.AC_3,
            ticket_type=TicketType.GENERAL,
        )

        # 1 station * 50 rs * 1 passenger = 50
        assert price == Decimal("50")

    def test_edge_case_full_route(self):
        """Test edge case: Travel the full route."""
        strategy = FixPricingStrategy()
        stations = ["S1", "S2", "S3", "S4", "S5"]
        train = Train("1234", stations, strategy)
        calculator = TicketPriceCalculator([train])

        price = calculator.calculate(
            train_number="1234",
            number_of_passengers=1,
            from_station="S1",
            to_station="S5",
            coach_type=CoachType.SLEEPER,
            ticket_type=TicketType.GENERAL,
        )

        # 4 stations * 30 rs * 1 passenger = 120
        assert price == Decimal("120")

    def test_error_handling_invalid_train(self):
        """Test error handling for invalid train number."""
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C"], strategy)
        calculator = TicketPriceCalculator([train])

        with pytest.raises(ValueError, match="Train not found: 9999"):
            calculator.calculate(
                train_number="9999",
                number_of_passengers=1,
                from_station="A",
                to_station="C",
                coach_type=CoachType.AC_3,
            )

    def test_error_handling_invalid_route(self):
        """Test error handling for invalid route."""
        strategy = FixPricingStrategy()
        train = Train("1234", ["Mumbai", "Surat", "Kota"], strategy)
        calculator = TicketPriceCalculator([train])

        with pytest.raises(ValueError, match="Station not found in route"):
            calculator.calculate(
                train_number="1234",
                number_of_passengers=1,
                from_station="Delhi",
                to_station="Kota",
                coach_type=CoachType.AC_3,
            )

    def test_error_handling_reverse_route(self):
        """Test error handling for reverse route."""
        strategy = FixPricingStrategy()
        train = Train("1234", ["A", "B", "C", "D"], strategy)
        calculator = TicketPriceCalculator([train])

        with pytest.raises(ValueError, match="Invalid route"):
            calculator.calculate(
                train_number="1234",
                number_of_passengers=1,
                from_station="D",
                to_station="A",
                coach_type=CoachType.AC_3,
            )
