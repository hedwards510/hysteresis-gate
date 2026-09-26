import unittest

from hysteresis_gate.core import HysteresisGate


class TestHysteresisGate(unittest.TestCase):
    def test_rise_opens_gate(self):
        g = HysteresisGate(rise=10.0, fall=5.0)
        self.assertFalse(g.update(8.0))
        self.assertTrue(g.update(10.0))

    def test_fall_closes_gate(self):
        g = HysteresisGate(rise=10.0, fall=5.0)
        g.update(12.0)
        self.assertTrue(g.update(7.0))
        self.assertFalse(g.update(5.0))

    def test_band_is_sticky(self):
        g = HysteresisGate(rise=10.0, fall=5.0)
        g.update(12.0)
        self.assertTrue(g.state)
        self.assertTrue(g.update(7.0))
        self.assertTrue(g.update(6.0))
        self.assertFalse(g.update(5.0))

    def test_band_sticky_from_below(self):
        g = HysteresisGate(rise=10.0, fall=5.0)
        g.update(2.0)
        self.assertFalse(g.state)
        self.assertFalse(g.update(6.0))
        self.assertFalse(g.update(7.0))
        self.assertTrue(g.update(10.0))

    def test_rise_below_fall_is_rejected(self):
        with self.assertRaises(ValueError):
            HysteresisGate(rise=3.0, fall=5.0)

    def test_equal_thresholds_allowed(self):
        g = HysteresisGate(rise=7.0, fall=7.0)
        self.assertFalse(g.update(6.9))
        self.assertTrue(g.update(7.0))
        self.assertFalse(g.update(6.9))

    def test_initial_state_open(self):
        g = HysteresisGate(rise=10.0, fall=5.0, initial=True)
        self.assertTrue(g.state)
        self.assertTrue(g.update(6.0))
        self.assertFalse(g.update(5.0))

    def test_reset_returns_to_closed(self):
        g = HysteresisGate(rise=10.0, fall=5.0)
        g.update(12.0)
        g.reset()
        self.assertFalse(g.state)
        self.assertFalse(g.update(7.0))

    def test_reset_with_initial(self):
        g = HysteresisGate(rise=10.0, fall=5.0)
        g.update(12.0)
        g.reset(initial=True)
        self.assertTrue(g.state)
        self.assertTrue(g.update(7.0))

    def test_update_returns_state(self):
        g = HysteresisGate(rise=10.0, fall=5.0)
        self.assertFalse(g.update(0.0))
        self.assertTrue(g.update(10.0))
        self.assertTrue(g.update(10.0))
        self.assertFalse(g.update(5.0))

    def test_negative_thresholds(self):
        g = HysteresisGate(rise=-5.0, fall=-10.0)
        self.assertFalse(g.update(-7.0))
        self.assertTrue(g.update(-5.0))
        self.assertTrue(g.update(-7.0))
        self.assertFalse(g.update(-10.0))

    def test_zero_band_degenerate_threshold(self):
        g = HysteresisGate(rise=0.0, fall=0.0)
        self.assertFalse(g.update(-0.001))
        self.assertTrue(g.update(0.0))
        self.assertFalse(g.update(-0.001))

    def test_state_property_is_read_only(self):
        g = HysteresisGate(rise=10.0, fall=5.0)
        with self.assertRaises(AttributeError):
            g.state = True


if __name__ == "__main__":
    unittest.main()
