"""Expected delivery costs under explicit independent-success assumptions."""
from __future__ import annotations

import math


def expected_cost(*, deliveries, acceptance_probability, generation_price,
                  review_seconds, editing_minutes_per_delivery, hourly_labor_price):
    values = [acceptance_probability, generation_price, review_seconds,
              editing_minutes_per_delivery, hourly_labor_price]
    if isinstance(deliveries, bool) or not isinstance(deliveries, int) or deliveries <= 0:
        raise ValueError('deliveries must be a positive integer')
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) for value in values):
        raise ValueError('All assumptions must be finite numeric values')
    if not 0 < acceptance_probability <= 1:
        raise ValueError('acceptance_probability must be in (0, 1]')
    if any(value < 0 for value in values[1:]):
        raise ValueError('Prices and time assumptions must be non-negative')
    attempts = deliveries / acceptance_probability
    generation = attempts * generation_price
    review = attempts * review_seconds / 3600 * hourly_labor_price
    editing = deliveries * editing_minutes_per_delivery / 60 * hourly_labor_price
    total = generation + review + editing
    return {'expected_generations': attempts, 'generation_cost': generation,
            'review_cost': review, 'editing_cost': editing, 'total_cost': total,
            'cost_per_delivery': total / deliveries}
