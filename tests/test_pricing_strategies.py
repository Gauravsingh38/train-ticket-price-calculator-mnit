"""Unit tests for pricing strategies."""

from decimal import Decimal

import pytest

from src.pricing_strategies import (
    DistanceBasedPricingStrategy,
    FixPricingStrategy,
    PremiumStationPricingStrategy,
)
from src.types import CoachType, TicketType


class TestFixPricingStrategy:
    """Test cases for FixPricingStrategy."""

    def test_general_ticket_3ac_single_passenger(self):
        """Test General ticket pricing for 3AC coach with single passenger."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Sawai Madhopur", "Jaipur"]

        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="Kota",
            to_station="Jaipur",
            stations=stations,
        )

        # 2 stations between Kota and Jaipur * 50 rs * 1 passenger = 100
        assert price == Decimal("100")

    def test_general_ticket_3ac_multiple_passengers(self):
        """Test General ticket pricing for 3AC coach with multiple passengers."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Sawai Madhopur", "Jaipur"]

        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=2,
            from_station="Kota",
            to_station="Jaipur",
            stations=stations,
        )

        # 2 stations * 50 rs * 2 passengers = 200
        assert price == Decimal("200")

    def test_tatkal_ticket_3ac_single_passenger(self):
        """Test Tatkal ticket pricing for 3AC coach with single passenger."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Sawai Madhopur", "Jaipur"]

        price = strategy.calculate_price(
            ticket_type=TicketType.TATKAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="Kota",
            to_station="Jaipur",
            stations=stations,
        )

        # 2 stations * 100 rs * 1 passenger = 200
        assert price == Decimal("200")

    def test_general_ticket_sleeper_single_passenger(self):
        """Test General ticket pricing for Sleeper coach with single passenger."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Sawai Madhopur", "Jaipur"]

        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.SLEEPER,
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Jaipur",
            stations=stations,
        )

        # 4 stations * 30 rs * 1 passenger = 120
        assert price == Decimal("120")

    def test_tatkal_ticket_sleeper_single_passenger(self):
        """Test Tatkal ticket pricing for Sleeper coach with single passenger."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Sawai Madhopur", "Jaipur"]

        price = strategy.calculate_price(
            ticket_type=TicketType.TATKAL,
            coach_type=CoachType.SLEEPER,
            number_of_passengers=2,
            from_station="Surat",
            to_station="Sawai Madhopur",
            stations=stations,
        )

        # 2 stations * 50 rs * 2 passengers = 200
        assert price == Decimal("200")

    def test_general_ticket_2ac_single_passenger(self):
        """Test General ticket pricing for 2AC coach with single passenger."""
        strategy = FixPricingStrategy()
        stations = ["A", "B", "C", "D"]

        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_2,
            number_of_passengers=1,
            from_station="A",
            to_station="D",
            stations=stations,
        )

        # 3 stations * 70 rs * 1 passenger = 210
        assert price == Decimal("210")

    def test_tatkal_ticket_2ac_single_passenger(self):
        """Test Tatkal ticket pricing for 2AC coach with single passenger."""
        strategy = FixPricingStrategy()
        stations = ["A", "B", "C"]

        price = strategy.calculate_price(
            ticket_type=TicketType.TATKAL,
            coach_type=CoachType.AC_2,
            number_of_passengers=3,
            from_station="A",
            to_station="C",
            stations=stations,
        )

        # 2 stations * 140 rs * 3 passengers = 840
        assert price == Decimal("840")

    def test_invalid_route_order(self):
        """Test error when from_station comes after to_station."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Jaipur"]

        with pytest.raises(ValueError, match="Invalid route"):
            strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=CoachType.AC_3,
                number_of_passengers=1,
                from_station="Jaipur",
                to_station="Mumbai",
                stations=stations,
            )

    def test_invalid_from_station(self):
        """Test error when from_station is not present in stations."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Jaipur"]

        with pytest.raises(ValueError, match="Station not found in route: CBD"):
            strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=CoachType.AC_3,
                number_of_passengers=1,
                from_station="CBD",
                to_station="Jaipur",
                stations=stations,
            )

    def test_invalid_to_station(self):
        """Test error when to_station is not present in stations."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota", "Jaipur"]

        with pytest.raises(ValueError, match="Station not found in route: Kolkata"):
            strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=CoachType.AC_3,
                number_of_passengers=1,
                from_station="Mumbai",
                to_station="Kolkata",
                stations=stations,
            )

    def test_same_from_and_to_station(self):
        """Test error when from and to stations are the same."""
        strategy = FixPricingStrategy()
        stations = ["Mumbai", "Surat", "Kota"]

        with pytest.raises(ValueError, match="Invalid route"):
            strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=CoachType.AC_3,
                number_of_passengers=1,
                from_station="Kota",
                to_station="Kota",
                stations=stations,
            )

    def test_general_ticket_all_coach_types(self):
        """Test all coach types with General ticket."""
        strategy = FixPricingStrategy()
        stations = ["A", "B", "C"]

        # Test each coach type
        expected_prices = {
            CoachType.AC_3: Decimal("100"),  # 2 * 50
            CoachType.SLEEPER: Decimal("60"),  # 2 * 30
            CoachType.AC_2: Decimal("140"),  # 2 * 70
            CoachType.AC_1: Decimal("200"),  # 2 * 100
            CoachType.GENERAL: Decimal("40"),  # 2 * 20
        }

        for coach_type, expected_price in expected_prices.items():
            price = strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=coach_type,
                number_of_passengers=1,
                from_station="A",
                to_station="C",
                stations=stations,
            )
            assert price == expected_price

    def test_tatkal_ticket_all_coach_types(self):
        """Test all coach types with Tatkal ticket."""
        strategy = FixPricingStrategy()
        stations = ["A", "B", "C"]

        # Test each coach type
        expected_prices = {
            CoachType.AC_3: Decimal("200"),  # 2 * 100
            CoachType.SLEEPER: Decimal("100"),  # 2 * 50
            CoachType.AC_2: Decimal("280"),  # 2 * 140
            CoachType.AC_1: Decimal("400"),  # 2 * 200
            CoachType.GENERAL: Decimal("80"),  # 2 * 40
        }

        for coach_type, expected_price in expected_prices.items():
            price = strategy.calculate_price(
                ticket_type=TicketType.TATKAL,
                coach_type=coach_type,
                number_of_passengers=1,
                from_station="A",
                to_station="C",
                stations=stations,
            )
            assert price == expected_price


class TestDistanceBasedPricingStrategy:
    """Test cases for DistanceBasedPricingStrategy."""

    def test_distance_based_general_ticket(self):
        """
        Test distance-based pricing with General ticket.
        Route: Mumbai (0km) -> Kota (800km) -> Jaipur (1000km).
        Travel: Kota to Jaipur (200km), 1 passenger, Sleeper General.
        Expected: 200 km × ₹1.0 (base) × 1.0 (Sleeper) × 1.0 (General) = ₹200
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Kota", Decimal("800")),
            ("Jaipur", Decimal("200")),
        ]
        strategy = DistanceBasedPricingStrategy(station_distances)
        stations = ["Mumbai", "Kota", "Jaipur"]

        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.SLEEPER,
            number_of_passengers=1,
            from_station="Kota",
            to_station="Jaipur",
            stations=stations,
        )

        assert price == Decimal("200")

    def test_distance_based_tatkal_ticket(self):
        """
        Test distance-based pricing with Tatkal ticket.
        Route: Mumbai (0km) -> Jaipur (1000km).
        Travel: Mumbai to Jaipur (1000km), 2 passengers, 3AC Tatkal.
        Expected: 1000 km × ₹1.0 (base) × 1.5 (3AC) × 2.0 (Tatkal) × 2 = ₹6000
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Jaipur", Decimal("1000")),
        ]
        strategy = DistanceBasedPricingStrategy(station_distances)
        stations = ["Mumbai", "Jaipur"]

        price = strategy.calculate_price(
            ticket_type=TicketType.TATKAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=2,
            from_station="Mumbai",
            to_station="Jaipur",
            stations=stations,
        )

        assert price == Decimal("6000")

    def test_distance_based_general_ticket_station_not_in_list(self):
        """
        Test error when station is not in the station list.
        Verifies that proper error is raised for unknown stations.
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Jaipur", Decimal("1000")),
        ]
        strategy = DistanceBasedPricingStrategy(station_distances)
        stations = ["Mumbai", "Delhi"]

        with pytest.raises(ValueError, match="Station not found: Delhi"):
            strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=CoachType.SLEEPER,
                number_of_passengers=1,
                from_station="Mumbai",
                to_station="Delhi",
                stations=stations,
            )

    def test_distance_based_general_ticket_same_from_and_to_station(self):
        """
        Test error when from_station and to_station are the same.
        Verifies that proper error is raised for invalid same-station routes.
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Jaipur", Decimal("1000")),
        ]
        strategy = DistanceBasedPricingStrategy(station_distances)
        stations = ["Mumbai", "Jaipur"]

        with pytest.raises(
            ValueError, match="Invalid route: Mumbai must come before Mumbai"
        ):
            strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=CoachType.SLEEPER,
                number_of_passengers=1,
                from_station="Mumbai",
                to_station="Mumbai",
                stations=stations,
            )

    def test_distance_based_general_ticket_reverse_route(self):
        """
        Test error when trying to travel in reverse direction.
        Route: Mumbai (0km) -> Surat (300km) -> Kota (800km).
        Travel: Kota to Mumbai (reverse direction) should raise error.
        Expected: ValueError indicating invalid route order.
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("300")),
            ("Kota", Decimal("500")),
        ]
        strategy = DistanceBasedPricingStrategy(station_distances)
        stations = ["Mumbai", "Surat", "Kota"]

        with pytest.raises(
            ValueError, match="Invalid route: Kota must come before Mumbai"
        ):
            strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=CoachType.SLEEPER,
                number_of_passengers=1,
                from_station="Kota",
                to_station="Mumbai",
                stations=stations,
            )

    def test_distance_based_intermediate_stations(self):
        """
        Test distance calculation between intermediate stations.
        Route: A (0km) -> B (100km) -> C (150km) -> D (300km).
        Travel: B to C (50km), 1 passenger, Sleeper General.
        Expected: 50 km × ₹1.0 (base) × 1.0 (Sleeper) × 1.0 (General) = ₹50
        """
        station_distances = [
            ("A", Decimal("0")),
            ("B", Decimal("100")),
            ("C", Decimal("50")),
            ("D", Decimal("150")),
        ]
        strategy = DistanceBasedPricingStrategy(station_distances)
        stations = ["A", "B", "C", "D"]

        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.SLEEPER,
            number_of_passengers=1,
            from_station="B",
            to_station="C",
            stations=stations,
        )

        assert price == Decimal("50")

    def test_distance_based_custom_pricing(self):
        """
        Test DistanceBasedPricingStrategy with custom pricing parameters.
        Uses custom base_rate_per_km (₹2.0) and custom coach_multiplier
        (2.0 for 3AC). Route: Mumbai (0km) -> Jaipur (1000km).
        Travel: Mumbai to Jaipur (1000km), 1 passenger, 3AC General.
        Expected: 1000 km × ₹2.0 (custom base) × 2.0 (custom 3AC) × 1.0 = ₹4000
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Jaipur", Decimal("1000")),
        ]
        custom_coach_multiplier = {
            CoachType.AC_3: Decimal("2.0"),
            CoachType.SLEEPER: Decimal("1.0"),
            CoachType.AC_2: Decimal("2.5"),
            CoachType.AC_1: Decimal("3.5"),
            CoachType.GENERAL: Decimal("0.5"),
        }
        strategy = DistanceBasedPricingStrategy(
            station_distances=station_distances,
            base_rate_per_km=Decimal("2.0"),
            coach_multiplier=custom_coach_multiplier,
        )
        stations = ["Mumbai", "Jaipur"]

        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Jaipur",
            stations=stations,
        )

        assert price == Decimal("4000")

    def test_distance_based_reverse_adjacent_stations(self):
        """
        Test error when trying to travel from later station to earlier adjacent station.
        Route: A (0km) -> B (100km).
        Travel: B to A (reverse) should raise error.
        """
        station_distances = [
            ("A", Decimal("0")),
            ("B", Decimal("100")),
        ]
        strategy = DistanceBasedPricingStrategy(station_distances)
        stations = ["A", "B"]

        with pytest.raises(ValueError, match="Invalid route: B must come before A"):
            strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=CoachType.SLEEPER,
                number_of_passengers=1,
                from_station="B",
                to_station="A",
                stations=stations,
            )

    def test_distance_based_reverse_long_route(self):
        """
        Test error when trying to travel reverse on long route.
        Route: Mumbai (0km) -> Surat (300km) -> Kota (800km) -> Jaipur (1200km).
        Travel: Jaipur to Mumbai (reverse) should raise error.
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("300")),
            ("Kota", Decimal("500")),
            ("Jaipur", Decimal("400")),
        ]
        strategy = DistanceBasedPricingStrategy(station_distances)
        stations = ["Mumbai", "Surat", "Kota", "Jaipur"]

        with pytest.raises(
            ValueError, match="Invalid route: Jaipur must come before Mumbai"
        ):
            strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=CoachType.AC_3,
                number_of_passengers=1,
                from_station="Jaipur",
                to_station="Mumbai",
                stations=stations,
            )

    def test_distance_based_reverse_intermediate_stations(self):
        """
        Test error when trying to travel reverse between intermediate stations.
        Route: Mumbai (0km) -> Surat (300km) -> Kota (800km) -> Jaipur (1200km).
        Travel: Kota to Surat (reverse) should raise error.
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("300")),
            ("Kota", Decimal("500")),
            ("Jaipur", Decimal("400")),
        ]
        strategy = DistanceBasedPricingStrategy(station_distances)
        stations = ["Mumbai", "Surat", "Kota", "Jaipur"]

        with pytest.raises(
            ValueError, match="Invalid route: Kota must come before Surat"
        ):
            strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=CoachType.SLEEPER,
                number_of_passengers=1,
                from_station="Kota",
                to_station="Surat",
                stations=stations,
            )

    def test_distance_based_multiple_passengers(self):
        """
        Test distance-based pricing with multiple passengers.
        Route: Mumbai (0km) -> Kota (800km).
        Travel: Mumbai to Kota (800km), 3 passengers, AC_2 Tatkal.
        Expected: 800 km × ₹1.0 (base) × 2.0 (AC_2) × 2.0 (Tatkal) × 3 = ₹9600
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Kota", Decimal("800")),
        ]
        strategy = DistanceBasedPricingStrategy(station_distances)
        stations = ["Mumbai", "Kota"]

        price = strategy.calculate_price(
            ticket_type=TicketType.TATKAL,
            coach_type=CoachType.AC_2,
            number_of_passengers=3,
            from_station="Mumbai",
            to_station="Kota",
            stations=stations,
        )

        assert price == Decimal("9600")

    def test_distance_based_all_coach_types(self):
        """
        Test distance-based pricing with all coach types.
        Route: A (0km) -> B (100km).
        Travel: A to B (100km), 1 passenger, General ticket.
        """
        station_distances = [
            ("A", Decimal("0")),
            ("B", Decimal("100")),
        ]
        strategy = DistanceBasedPricingStrategy(station_distances)
        stations = ["A", "B"]

        # Test all coach types
        expected_prices = {
            CoachType.AC_3: Decimal("150"),  # 100 × 1.0 × 1.5 × 1.0 = 150
            CoachType.SLEEPER: Decimal("100"),  # 100 × 1.0 × 1.0 × 1.0 = 100
            CoachType.AC_2: Decimal("200"),  # 100 × 1.0 × 2.0 × 1.0 = 200
            CoachType.AC_1: Decimal("300"),  # 100 × 1.0 × 3.0 × 1.0 = 300
            CoachType.GENERAL: Decimal("50"),  # 100 × 1.0 × 0.5 × 1.0 = 50
        }

        for coach_type, expected_price in expected_prices.items():
            price = strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=coach_type,
                number_of_passengers=1,
                from_station="A",
                to_station="B",
                stations=stations,
            )
            assert price == expected_price


class TestCustomPricing:
    """Test cases for custom pricing configurations."""

    def test_custom_pricing_general_ticket(self):
        """
        Test FixPricingStrategy with custom pricing rates.
        Uses custom general_pricing (₹75 for 3AC) and custom tatkal_pricing
        (₹150 for 3AC). Route: A to C (2 stations), 1 passenger, 3AC General.
        Expected: 2 stations × ₹75 (custom 3AC General) = ₹150
        """
        custom_general_pricing = {
            CoachType.AC_3: Decimal("75"),
            CoachType.SLEEPER: Decimal("45"),
            CoachType.AC_2: Decimal("100"),
            CoachType.AC_1: Decimal("150"),
            CoachType.GENERAL: Decimal("30"),
        }
        custom_tatkal_pricing = {
            CoachType.AC_3: Decimal("150"),
            CoachType.SLEEPER: Decimal("75"),
            CoachType.AC_2: Decimal("200"),
            CoachType.AC_1: Decimal("300"),
            CoachType.GENERAL: Decimal("60"),
        }
        strategy = FixPricingStrategy(
            general_pricing=custom_general_pricing, tatkal_pricing=custom_tatkal_pricing
        )
        stations = ["A", "B", "C"]

        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            stations=stations,
        )

        assert price == Decimal("150")

    def test_custom_pricing_tatkal_ticket(self):
        """
        Test FixPricingStrategy with custom Tatkal pricing rates.
        Uses custom tatkal_pricing (₹150 for 3AC).
        Route: A to C (2 stations), 1 passenger, 3AC Tatkal.
        Expected: 2 stations × ₹150 (custom 3AC Tatkal) = ₹300
        """
        custom_general_pricing = {
            CoachType.AC_3: Decimal("75"),
            CoachType.SLEEPER: Decimal("45"),
            CoachType.AC_2: Decimal("100"),
            CoachType.AC_1: Decimal("150"),
            CoachType.GENERAL: Decimal("30"),
        }
        custom_tatkal_pricing = {
            CoachType.AC_3: Decimal("150"),
            CoachType.SLEEPER: Decimal("75"),
            CoachType.AC_2: Decimal("200"),
            CoachType.AC_1: Decimal("300"),
            CoachType.GENERAL: Decimal("60"),
        }
        strategy = FixPricingStrategy(
            general_pricing=custom_general_pricing, tatkal_pricing=custom_tatkal_pricing
        )
        stations = ["A", "B", "C"]

        price = strategy.calculate_price(
            ticket_type=TicketType.TATKAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="A",
            to_station="C",
            stations=stations,
        )

        assert price == Decimal("300")


class TestPremiumStationPricingStrategy:
    """Test cases for PremiumStationPricingStrategy (not yet implemented)."""

    def test_regular_to_regular_station_no_surcharge(self):
        """
        Test pricing from regular station to regular station.
        Route: Mumbai (non-premium) to Surat (non-premium): 300km
        Expected: Base price with no premium surcharge
        Formula: 300 * 1.0 * 1.5 (AC3) * 1.0 (General) * 1 passenger = ₹450
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("300")),
            ("Jaipur", Decimal("900")),
        ]
        premium_stations = {
            "Jaipur": Decimal("0.30"),  # Only Jaipur is premium
        }

        strategy = PremiumStationPricingStrategy(
            station_distances=station_distances,
            premium_stations=premium_stations,
        )
        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Surat",
            stations=["Mumbai", "Surat", "Jaipur"],
        )

        assert price == Decimal("450")

    def test_premium_tier1_to_regular_station(self):
        """
        Test pricing from TIER_1 premium station to regular station.
        Route: Mumbai (TIER_1, 50%) to Surat (non-premium): 300km
        Expected: Base price + 50% surcharge
        Base: 300 * 1.0 * 1.5 (AC3) * 1.0 (General) = ₹450
        Surcharge: 50% of ₹450 = ₹225
        Total: ₹450 + ₹225 = ₹675
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("300")),
        ]
        premium_stations = {
            "Mumbai": Decimal("0.50"),  # TIER_1: 50% surcharge
        }

        strategy = PremiumStationPricingStrategy(
            station_distances=station_distances,
            premium_stations=premium_stations,
        )
        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Surat",
            stations=["Mumbai", "Surat"],
        )

        assert price == Decimal("675")

    def test_regular_to_premium_tier2_station(self):
        """
        Test pricing from regular station to TIER_2 premium station.
        Route: Surat (non-premium) to Jaipur (TIER_2, 30%): 900km
        Expected: Base price + 30% surcharge
        Base: 900 * 1.0 * 1.5 (AC3) * 1.0 (General) = ₹1350
        Surcharge: 30% of ₹1350 = ₹405
        Total: ₹1350 + ₹405 = ₹1755
        """
        station_distances = [
            ("Surat", Decimal("0")),
            ("Jaipur", Decimal("900")),
        ]
        premium_stations = {
            "Jaipur": Decimal("0.30"),  # TIER_2: 30% surcharge
        }

        strategy = PremiumStationPricingStrategy(
            station_distances=station_distances,
            premium_stations=premium_stations,
        )
        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="Surat",
            to_station="Jaipur",
            stations=["Surat", "Jaipur"],
        )

        assert price == Decimal("1755")

    def test_premium_tier1_to_premium_tier1_both_surcharges(self):
        """
        Test pricing from TIER_1 premium to TIER_1 premium (both premium).
        Route: Mumbai (TIER_1, 50%) to Delhi (TIER_1, 50%): 1400km
        Expected: Base price + from surcharge + to surcharge
        Base: 1400 * 1.0 * 1.5 (AC3) * 1.0 (General) = ₹2100
        From surcharge: 50% of ₹2100 = ₹1050
        To surcharge: 50% of ₹2100 = ₹1050
        Total: ₹2100 + ₹1050 + ₹1050 = ₹4200
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Delhi", Decimal("1400")),
        ]
        premium_stations = {
            "Mumbai": Decimal("0.50"),  # TIER_1: 50% surcharge
            "Delhi": Decimal("0.50"),  # TIER_1: 50% surcharge
        }

        strategy = PremiumStationPricingStrategy(
            station_distances=station_distances,
            premium_stations=premium_stations,
        )
        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Delhi",
            stations=["Mumbai", "Delhi"],
        )

        assert price == Decimal("4200")

    def test_premium_tier1_to_premium_tier2_different_surcharges(self):
        """
        Test pricing from TIER_1 to TIER_2 premium (different tiers).
        Route: Mumbai (TIER_1, 50%) to Jaipur (TIER_2, 30%): 1200km
        Expected: Base price + from surcharge (50%) + to surcharge (30%)
        Base: 1200 * 1.0 * 1.5 (AC3) * 1.0 (General) = ₹1800
        From surcharge: 50% of ₹1800 = ₹900
        To surcharge: 30% of ₹1800 = ₹540
        Total: ₹1800 + ₹900 + ₹540 = ₹3240
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Jaipur", Decimal("1200")),
        ]
        premium_stations = {
            "Mumbai": Decimal("0.50"),  # TIER_1: 50% surcharge
            "Jaipur": Decimal("0.30"),  # TIER_2: 30% surcharge
        }

        strategy = PremiumStationPricingStrategy(
            station_distances=station_distances,
            premium_stations=premium_stations,
        )
        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Jaipur",
            stations=["Mumbai", "Jaipur"],
        )

        assert price == Decimal("3240")

    def test_premium_tier3_tourist_destination(self):
        """
        Test pricing with TIER_3 premium (tourist destination).
        Route: Pune (non-premium) to Goa (TIER_3, 20%): 500km
        Expected: Base price + 20% surcharge for tourist destination
        Base: 500 * 1.0 * 1.5 (AC3) * 1.0 (General) = ₹750
        Surcharge: 20% of ₹750 = ₹150
        Total: ₹750 + ₹150 = ₹900
        """
        station_distances = [
            ("Pune", Decimal("0")),
            ("Goa", Decimal("500")),
        ]
        premium_stations = {
            "Goa": Decimal("0.20"),  # TIER_3: 20% surcharge (tourist spot)
        }

        strategy = PremiumStationPricingStrategy(
            station_distances=station_distances,
            premium_stations=premium_stations,
        )
        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="Pune",
            to_station="Goa",
            stations=["Pune", "Goa"],
        )

        assert price == Decimal("900")

    def test_premium_with_multiple_passengers(self):
        """
        Test premium pricing with multiple passengers.
        Route: Mumbai (TIER_1, 50%) to Surat (non-premium): 300km, 3 passengers
        Expected: (Base price + surcharge) * passengers
        Base: 300 * 1.0 * 1.5 (AC3) * 1.0 (General) = ₹450
        Surcharge: 50% of ₹450 = ₹225
        Per passenger: ₹450 + ₹225 = ₹675
        Total: ₹675 * 3 = ₹2025
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("300")),
        ]
        premium_stations = {
            "Mumbai": Decimal("0.50"),  # TIER_1: 50% surcharge
        }

        strategy = PremiumStationPricingStrategy(
            station_distances=station_distances,
            premium_stations=premium_stations,
        )
        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=3,
            from_station="Mumbai",
            to_station="Surat",
            stations=["Mumbai", "Surat"],
        )

        assert price == Decimal("2025")

    def test_premium_with_tatkal_ticket(self):
        """
        Test premium pricing with Tatkal ticket type.
        Route: Mumbai (TIER_1, 50%) to Surat (non-premium): 300km, Tatkal
        Expected: Base price (with Tatkal multiplier) + premium surcharge
        Base: 300 * 1.0 * 1.5 (AC3) * 2.0 (Tatkal) = ₹900
        Surcharge: 50% of ₹900 = ₹450
        Total: ₹900 + ₹450 = ₹1350
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("300")),
        ]
        premium_stations = {
            "Mumbai": Decimal("0.50"),  # TIER_1: 50% surcharge
        }

        strategy = PremiumStationPricingStrategy(
            station_distances=station_distances,
            premium_stations=premium_stations,
        )
        price = strategy.calculate_price(
            ticket_type=TicketType.TATKAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Surat",
            stations=["Mumbai", "Surat"],
        )

        assert price == Decimal("1350")

    def test_premium_with_different_coach_types(self):
        """
        Test premium pricing with different coach types.
        Route: Mumbai (TIER_1, 50%) to Surat (non-premium): 300km
        Verifies that premium surcharge applies correctly to different coach types.
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("300")),
        ]
        premium_stations = {
            "Mumbai": Decimal("0.50"),  # TIER_1: 50% surcharge
        }

        # Expected calculations for each coach type:
        # SLEEPER: Base = 300 * 1.0 * 1.0 = ₹300, Surcharge = 50% = ₹150, Total = ₹450
        # AC_3: Base = 300 * 1.0 * 1.5 = ₹450, Surcharge = 50% = ₹225, Total = ₹675
        # AC_2: Base = 300 * 1.0 * 2.0 = ₹600, Surcharge = 50% = ₹300, Total = ₹900

        strategy = PremiumStationPricingStrategy(
            station_distances=station_distances,
            premium_stations=premium_stations,
        )

        expected_prices = {
            CoachType.SLEEPER: Decimal("450"),
            CoachType.AC_3: Decimal("675"),
            CoachType.AC_2: Decimal("900"),
        }

        for coach_type, expected_price in expected_prices.items():
            price = strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=coach_type,
                number_of_passengers=1,
                from_station="Mumbai",
                to_station="Surat",
                stations=["Mumbai", "Surat"],
            )
            assert price == expected_price

    def test_premium_intermediate_stations(self):
        """
        Test premium pricing with intermediate stations.
        Route: Mumbai (TIER_1, 50%) -> Surat (non-premium) -> Jaipur (TIER_2, 30%)
        Travel: Mumbai to Jaipur (skipping Surat)
        Expected: Base price + from surcharge (50%) + to surcharge (30%)
        Distance: 0 to 1200km = 1200km
        Base: 1200 * 1.0 * 1.5 (AC3) * 1.0 (General) = ₹1800
        From surcharge: 50% of ₹1800 = ₹900
        To surcharge: 30% of ₹1800 = ₹540
        Total: ₹1800 + ₹900 + ₹540 = ₹3240
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("300")),
            ("Jaipur", Decimal("900")),  # 900km from Surat, 1200km total from Mumbai
        ]
        premium_stations = {
            "Mumbai": Decimal("0.50"),  # TIER_1: 50% surcharge
            "Jaipur": Decimal("0.30"),  # TIER_2: 30% surcharge
        }

        strategy = PremiumStationPricingStrategy(
            station_distances=station_distances,
            premium_stations=premium_stations,
        )
        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Jaipur",
            stations=["Mumbai", "Surat", "Jaipur"],
        )

        assert price == Decimal("3240")

    def test_premium_reverse_route_error(self):
        """
        Test error when trying to travel in reverse direction with premium stations.
        Route: Mumbai (TIER_1) -> Jaipur (TIER_2)
        Travel: Jaipur to Mumbai (reverse) should raise ValueError
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Jaipur", Decimal("1200")),
        ]
        premium_stations = {
            "Mumbai": Decimal("0.50"),
            "Jaipur": Decimal("0.30"),
        }

        strategy = PremiumStationPricingStrategy(
            station_distances=station_distances,
            premium_stations=premium_stations,
        )

        # This should raise ValueError for reverse route
        with pytest.raises(ValueError, match="Invalid route"):
            strategy.calculate_price(
                ticket_type=TicketType.GENERAL,
                coach_type=CoachType.AC_3,
                number_of_passengers=1,
                from_station="Jaipur",
                to_station="Mumbai",
                stations=["Mumbai", "Jaipur"],
            )

    def test_premium_station_not_in_distances_error(self):
        """
        Test error when premium station is not in station_distances.
        Should raise ValueError during initialization.
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("300")),
        ]
        premium_stations = {
            "Delhi": Decimal("0.50"),  # Delhi not in station_distances
        }

        # This should raise ValueError because Delhi is not in station_distances
        with pytest.raises(ValueError, match="not found in station_distances"):
            PremiumStationPricingStrategy(
                station_distances=station_distances,
                premium_stations=premium_stations,
            )

    def test_premium_invalid_surcharge_percentage_error(self):
        """
        Test error when premium surcharge is invalid (> 1.0 or < 0.0).
        Should raise ValueError during initialization.
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("300")),
        ]

        # Test surcharge > 1.0 (> 100%)
        premium_stations_high = {
            "Mumbai": Decimal("1.5"),  # 150% - invalid
        }

        # This should raise ValueError because surcharge > 1.0
        with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
            PremiumStationPricingStrategy(
                station_distances=station_distances,
                premium_stations=premium_stations_high,
            )

        # Test surcharge < 0.0 (negative)
        premium_stations_negative = {
            "Mumbai": Decimal("-0.1"),  # -10% - invalid
        }

        # This should raise ValueError because surcharge < 0.0
        with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
            PremiumStationPricingStrategy(
                station_distances=station_distances,
                premium_stations=premium_stations_negative,
            )

    def test_premium_custom_base_rate(self):
        """
        Test premium pricing with custom base rate per km.
        Route: Mumbai (TIER_1, 50%) to Surat (non-premium): 300km
        Custom base rate: ₹2.0 per km
        Expected: Base price (with custom rate) + premium surcharge
        Base: 300 * 2.0 * 1.5 (AC3) * 1.0 (General) = ₹900
        Surcharge: 50% of ₹900 = ₹450
        Total: ₹900 + ₹450 = ₹1350
        """
        station_distances = [
            ("Mumbai", Decimal("0")),
            ("Surat", Decimal("300")),
        ]
        premium_stations = {
            "Mumbai": Decimal("0.50"),  # TIER_1: 50% surcharge
        }

        strategy = PremiumStationPricingStrategy(
            station_distances=station_distances,
            premium_stations=premium_stations,
            base_rate_per_km=Decimal("2.0"),
        )
        price = strategy.calculate_price(
            ticket_type=TicketType.GENERAL,
            coach_type=CoachType.AC_3,
            number_of_passengers=1,
            from_station="Mumbai",
            to_station="Surat",
            stations=["Mumbai", "Surat"],
        )

        assert price == Decimal("1350")
