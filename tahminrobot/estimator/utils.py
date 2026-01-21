def estimate_price(square_meters: float, rooms: int, floor: int, age: int) -> float:
    """
    Simple heuristic-based estimator.

    Base assumptions:
    - base price per square meter: 2000
    - rooms increase value (3% per room)
    - upper floors increase value (2% per floor)
    - building age decreases value (1% per year)

    The final multiplier is 1 + rooms*0.03 + floor*0.02 - age*0.01
    Multiplier is clamped to at least 0.3 to avoid negative/absurd values.
    """
    # Increase base price per square meter to produce much higher estimates
    # (Demo: market-scale numbers for a higher-looking output)
    base_per_sqm = 10000.0
    base_price = square_meters * base_per_sqm

    # Strong positive effects for rooms and floors so estimates scale up significantly
    # Rooms: +8% per room, Floor: +5% per floor, Age reduces slightly (-0.8% per year)
    multiplier = 1.0 + rooms * 0.08 + floor * 0.05 - age * 0.008
    # clamp multiplier to a reasonable range
    if multiplier < 0.3:
        multiplier = 0.3
    # Allow a larger cap so high inputs can generate high estimates
    if multiplier > 8.0:
        multiplier = 8.0

    price = base_price * multiplier
    return round(price, 2)


def format_try(amount: float) -> str:
    """Format a float as Turkish Lira with dot thousand separators and comma decimals.

    Example: 1234567.89 -> '₺ 1.234.567,89'
    """
    try:
        s = format(float(amount), ",.2f")  # gives 1,234,567.89
    except Exception:
        s = str(amount)

    # convert to Turkish style: 1.234.567,89
    s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'₺ {s}'


def estimate_with_location(square_meters: float, rooms: int, floor: int, age: int, location_rating: int, transport: str) -> float:
    """
    Enhanced estimator including location rating and transport quality.

    - location_rating: 1..10, each point adds +2% to price
    - transport: 'kolay' -> +5%, 'orta' -> 0%, 'zor' -> -5%

    Returns a float price rounded to 2 decimals.
    """
    base = estimate_price(square_meters, rooms, floor, age)

    # Location rating is influential: each point adds +5% (1 -> 1.05, 10 -> +50%)
    loc_multiplier = location_rating * 0.05
    # transport choices have stronger impact now (easy +10%, hard -10%)
    transport_map = {'kolay': 0.10, 'orta': 0.0, 'zor': -0.10}
    transport_multiplier = transport_map.get(transport, 0.0)

    total_multiplier = 1.0 + loc_multiplier + transport_multiplier - 1.0
    # total_multiplier currently expresses additional relative change; apply to base
    price = base * (1 + loc_multiplier + transport_multiplier)

    return round(price, 2)


def average_estimates(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 2)
