import unittest
from datetime import datetime

from automation_logic import evaluate_action, get_thresholds


class AutomationLogicTests(unittest.TestCase):
    def test_window_a_thresholds_and_turn_on(self):
        now = datetime(2026, 7, 28, 6, 30, 0)
        thresholds = get_thresholds(now)

        self.assertTrue(thresholds["window_a"])
        self.assertEqual(thresholds["on_threshold"], 50)
        self.assertEqual(thresholds["off_threshold"], 20)

        decision = evaluate_action(55, "off", now)
        self.assertTrue(decision["turn_on"])
        self.assertFalse(decision["turn_off"])

    def test_window_b_thresholds_and_turn_on(self):
        now = datetime(2026, 7, 28, 9, 0, 0)
        thresholds = get_thresholds(now)

        self.assertFalse(thresholds["window_a"])
        self.assertEqual(thresholds["on_threshold"], 75)
        self.assertEqual(thresholds["off_threshold"], 60)

        decision = evaluate_action(80, "off", now)
        self.assertTrue(decision["turn_on"])
        self.assertFalse(decision["turn_off"])

    def test_turn_off_during_window_a(self):
        now = datetime(2026, 7, 28, 7, 0, 0)
        decision = evaluate_action(15, "on", now)

        self.assertFalse(decision["turn_on"])
        self.assertTrue(decision["turn_off"])

    def test_no_action_when_state_already_matches(self):
        now = datetime(2026, 7, 28, 6, 0, 0)
        decision = evaluate_action(55, "on", now)

        self.assertFalse(decision["turn_on"])
        self.assertFalse(decision["turn_off"])


if __name__ == "__main__":
    unittest.main()
