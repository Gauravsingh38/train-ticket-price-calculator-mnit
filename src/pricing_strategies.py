"""Pricing strategies for train ticket calculation."""

from abc import ABC, abstractmethod
from decimal import Decimal
from src.types import CoachType, TicketType


# ---------------------------------------------------------
# BASE STRATEGY CLASS
# ---------------------------------------------------------

class PricingStrategy(ABC):

    @abstractmethod
    def calculate_price(
        self,
        ticket_type: TicketType,
        coach_type: CoachType,
        number_of_passengers: int,
        from_station: str,
        to_station: str,
        stations: list[str],
    ) -> Decimal:
        pass


# ---------------------------------------------------------
# FIXED PRICE STRATEGY
# ---------------------------------------------------------

class FixPricingStrategy(PricingStrategy):
    """Fixed pricing strategy - price per station."""

    DEFAULT_GENERAL_PRICING: dict[CoachType, Decimal] = {
        CoachType.AC_3: Decimal("50"),
        CoachType.SLEEPER: Decimal("30"),
        CoachType.AC_2: Decimal("70"),
        CoachType.AC_1: Decimal("100"),
        CoachType.GENERAL: Decimal("20"),
    }

    DEFAULT_TATKAL_PRICING: dict[CoachType, Decimal] = {
        CoachType.AC_3: Decimal("100"),
        CoachType.SLEEPER: Decimal("50"),
        CoachType.AC_2: Decimal("140"),
        CoachType.AC_1: Decimal("200"),
        CoachType.GENERAL: Decimal("40"),
    }

    def __init__(self, general_pricing=None, tatkal_pricing=None):
        self.general_pricing = general_pricing or self.DEFAULT_GENERAL_PRICING.copy()
        self.tatkal_pricing = tatkal_pricing or self.DEFAULT_TATKAL_PRICING.copy()

    def calculate_price(
        self, ticket_type, coach_type, number_of_passengers,
        from_station, to_station, stations
    ):
        # station existence checks
        if from_station not in stations:
            raise ValueError(f"Station not found in route: {from_station}")
        if to_station not in stations:
            raise ValueError(f"Station not found in route: {to_station}")

        # same station
        if from_station == to_station:
            raise ValueError("Invalid route")

        # ordering check
        fi = stations.index(from_station)
        ti = stations.index(to_station)
        if fi > ti:
            raise ValueError("Invalid route")

        station_count = ti - fi

        pricing = (
            self.general_pricing
            if ticket_type == TicketType.GENERAL
            else self.tatkal_pricing
        )

        return pricing[coach_type] * station_count * number_of_passengers


# ---------------------------------------------------------
# DISTANCE BASED STRATEGY
# ---------------------------------------------------------

class DistanceBasedPricingStrategy(PricingStrategy):

    DEFAULT_BASE_RATE_PER_KM = Decimal("1.0")

    DEFAULT_COACH_MULTIPLIER = {
        CoachType.AC_3: Decimal("1.5"),
        CoachType.SLEEPER: Decimal("1.0"),
        CoachType.AC_2: Decimal("2.0"),
        CoachType.AC_1: Decimal("3.0"),
        CoachType.GENERAL: Decimal("0.5"),
    }

    DEFAULT_TICKET_MULTIPLIER = {
        TicketType.GENERAL: Decimal("1.0"),
        TicketType.TATKAL: Decimal("2.0"),
    }

    def __init__(self, station_distances, base_rate_per_km=None,
                 coach_multiplier=None, ticket_multiplier=None):

        # Build cumulative distances: each tuple is (station_name, distance_from_prev)
        self.cumulative_distances: dict[str, Decimal] = {}
        cumulative = Decimal("0")

        for station, dist in station_distances:
            cumulative += dist
            self.cumulative_distances[station] = cumulative

        self.base_rate_per_km = base_rate_per_km or self.DEFAULT_BASE_RATE_PER_KM
        self.coach_multiplier = coach_multiplier or self.DEFAULT_COACH_MULTIPLIER.copy()
        self.ticket_multiplier = ticket_multiplier or self.DEFAULT_TICKET_MULTIPLIER.copy()

    def calculate_price(
        self, ticket_type, coach_type, number_of_passengers,
        from_station, to_station, stations
    ):
        # station existence
        if from_station not in stations:
            raise ValueError(f"Station not found: {from_station}")
        if to_station not in stations:
            raise ValueError(f"Station not found: {to_station}")

        # same station
        if from_station == to_station:
            raise ValueError(f"Invalid route: {from_station} must come before {to_station}")

        # ordering check (reverse route)
        fi = stations.index(from_station)
        ti = stations.index(to_station)
        if fi > ti:
            raise ValueError(f"Invalid route: {from_station} must come before {to_station}")

        # ensure distances are known in cumulative_distances
        if from_station not in self.cumulative_distances:
            raise ValueError(f"Station not found: {from_station}")
        if to_station not in self.cumulative_distances:
            raise ValueError(f"Station not found: {to_station}")

        distance = abs(
            self.cumulative_distances[to_station]
            - self.cumulative_distances[from_station]
        )

        base = (
            distance
            * self.base_rate_per_km
            * self.coach_multiplier[coach_type]
            * self.ticket_multiplier[ticket_type]
        )

        return base * number_of_passengers


# ---------------------------------------------------------
# PREMIUM STATION PRICING STRATEGY
# ---------------------------------------------------------

class PremiumStationPricingStrategy(PricingStrategy):
    """Premium station surcharge logic."""

    DEFAULT_BASE_RATE_PER_KM = Decimal("1.0")
    DEFAULT_COACH_MULTIPLIER = DistanceBasedPricingStrategy.DEFAULT_COACH_MULTIPLIER
    DEFAULT_TICKET_MULTIPLIER = DistanceBasedPricingStrategy.DEFAULT_TICKET_MULTIPLIER

    def __init__(
        self,
        station_distances,
        premium_stations=None,
        base_rate_per_km=None,
        coach_multiplier=None,
        ticket_multiplier=None,
    ):
        # cumulative distances
        self.cumulative_distances: dict[str, Decimal] = {}
        cumulative = Decimal("0")

        for station, dist in station_distances:
            cumulative += dist
            self.cumulative_distances[station] = cumulative

        # Validate premium stations: must exist and surcharge in [0.0, 1.0]
        self.premium_stations: dict[str, Decimal] = {}
        if premium_stations:
            for st, pct in premium_stations.items():
                if st not in self.cumulative_distances:
                    raise ValueError(f"Premium station '{st}' not found in station_distances")
                if not (Decimal("0.0") <= pct <= Decimal("1.0")):
                    raise ValueError("Premium percentage must be between 0.0 and 1.0")
                self.premium_stations[st] = pct

        self.base_rate_per_km = base_rate_per_km or self.DEFAULT_BASE_RATE_PER_KM
        self.coach_multiplier = coach_multiplier or self.DEFAULT_COACH_MULTIPLIER.copy()
        self.ticket_multiplier = ticket_multiplier or self.DEFAULT_TICKET_MULTIPLIER.copy()

    def calculate_price(
        self,
        ticket_type,
        coach_type,
        number_of_passengers,
        from_station,
        to_station,
        stations,
    ):
        # station existence
        if from_station not in stations:
            raise ValueError(f"Station not found: {from_station}")
        if to_station not in stations:
            raise ValueError(f"Station not found: {to_station}")

        # same station
        if from_station == to_station:
            raise ValueError(f"Invalid route: {from_station} must come before {to_station}")

        # ordering check (reverse)
        fi = stations.index(from_station)
        ti = stations.index(to_station)
        if fi > ti:
            raise ValueError(f"Invalid route: {from_station} must come before {to_station}")

        # ensure distances present
        if from_station not in self.cumulative_distances:
            raise ValueError(f"Station not found: {from_station}")
        if to_station not in self.cumulative_distances:
            raise ValueError(f"Station not found: {to_station}")

        distance = abs(
            self.cumulative_distances[to_station]
            - self.cumulative_distances[from_station]
        )

        base_price = (
            distance
            * self.base_rate_per_km
            * self.coach_multiplier[coach_type]
            * self.ticket_multiplier[ticket_type]
        )

        from_pct = self.premium_stations.get(from_station, Decimal("0.0"))
        to_pct = self.premium_stations.get(to_station, Decimal("0.0"))

        surcharge = base_price * from_pct + base_price * to_pct

        return (base_price + surcharge) * number_of_passengers
