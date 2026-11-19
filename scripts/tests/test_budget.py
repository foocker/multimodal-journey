import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('budget', Path(__file__).resolve().parents[2] / 'algorithms/compute-budget/budget.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CostAssumptionTests(unittest.TestCase):
    def arguments(self):
        return {'deliveries': 10, 'acceptance_probability': 0.25, 'generation_price': 1.2,
                'review_seconds': 45, 'editing_minutes_per_delivery': 8, 'hourly_labor_price': 60}

    def test_known_budget_and_probability_boundary(self):
        result = MODULE.expected_cost(**self.arguments())
        self.assertAlmostEqual(result['total_cost'], 158)
        arguments = self.arguments()
        arguments['acceptance_probability'] = 1
        self.assertEqual(MODULE.expected_cost(**arguments)['expected_generations'], 10)

    def test_invalid_assumptions_do_not_produce_plausible_costs(self):
        for field, value in [('deliveries', 0), ('deliveries', True), ('acceptance_probability', 0),
                             ('acceptance_probability', 1.01), ('generation_price', -1),
                             ('hourly_labor_price', float('nan')), ('review_seconds', float('inf'))]:
            with self.subTest(field=field, value=value):
                arguments = self.arguments()
                arguments[field] = value
                with self.assertRaises(ValueError):
                    MODULE.expected_cost(**arguments)


if __name__ == '__main__':
    unittest.main()
