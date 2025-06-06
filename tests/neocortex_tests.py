import unittest
import json
from Neocortex import raw, primary, secondary


class TestNeocortex(unittest.TestCase):
    """Tests for Neocortex features using simulated data."""

    def test_raw_steps_json(self):
        data = json.dumps([
            {"timestamp": 1, "value": 2},
            {"timestamp": 2, "value": 3}
        ])
        events = raw.steps(data)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["value"], 2)

    def test_screen_active(self):
        events = [
            {"timestamp": 0, "representation": "locked"},
            {"timestamp": 10, "representation": "unlocked"},
            {"timestamp": 20, "representation": "locked"},
            {"timestamp": 30, "representation": "unlocked"},
            {"timestamp": 40, "representation": "screen_off"},
        ]
        intervals = primary.screen_active(events)
        self.assertEqual(intervals, [{"start": 10, "end": 20}, {"start": 30, "end": 40}])

    def test_step_count(self):
        events = [
            {"timestamp": 0, "value": 1},
            {"timestamp": 1000, "value": 2},
            {"timestamp": 86400000 + 1000, "value": 3},
        ]
        counts = secondary.step_count(events, start=0, end=86400000 * 2, resolution=86400000)
        self.assertEqual(counts[0]["value"], 3)
        self.assertEqual(counts[1]["value"], 3)

    def test_significant_locations_and_secondary(self):
        gps_events = [
            {"timestamp": 0, "latitude": 1.0, "longitude": 1.0},
            {"timestamp": 10, "latitude": 1.0, "longitude": 1.0},
            {"timestamp": 20, "latitude": 2.0, "longitude": 2.0},
            {"timestamp": 25, "latitude": 2.0, "longitude": 2.0},
        ]
        sig = primary.significant_locations(gps_events, start=0, end=30)
        self.assertEqual(len(sig["data"]), 2)
        self.assertEqual(sig["data"][0]["duration"], 20)
        ht = secondary.hometime(gps_events, start=0, end=30)
        self.assertEqual(ht["value"], 20)
        ent = secondary.entropy(gps_events, start=0, end=30)
        import math
        self.assertTrue(math.isclose(ent["value"], 0.6365141682948128, rel_tol=1e-6))

    def test_sample_formats(self):
        """Ensure functions handle records shaped like real sensor payloads."""
        step_event = {
            "sensor": "lamp.steps",
            "timestamp": 1000,
            "source": "com.google.android.gms",
            "type": "step_count",
            "unit": "count",
            "value": 5,
        }
        steps_loaded = raw.steps([step_event])
        self.assertEqual(len(steps_loaded), 1)
        self.assertEqual(steps_loaded[0]["value"], 5)

        counts = secondary.step_count(steps_loaded, start=0, end=86400000, resolution=86400000)
        self.assertEqual(counts[0]["value"], 5)

        device_events = [
            {
                "sensor": "lamp.device_state",
                "timestamp": 0,
                "battery_level": 0.5,
                "representation": "locked",
                "value": 2,
            },
            {
                "sensor": "lamp.device_state",
                "timestamp": 10,
                "battery_level": 0.5,
                "representation": "unlocked",
                "value": 3,
            },
            {
                "sensor": "lamp.device_state",
                "timestamp": 20,
                "battery_level": 0.5,
                "representation": "screen_off",
                "value": 1,
            },
        ]
        intervals = primary.screen_active(device_events)
        self.assertEqual(intervals, [{"start": 10, "end": 20}])

        gps_events = [
            {
                "sensor": "lamp.gps",
                "timestamp": 0,
                "accuracy": 135.6,
                "altitude": 179.4,
                "latitude": 1.0,
                "longitude": 1.0,
            },
            {
                "sensor": "lamp.gps",
                "timestamp": 10,
                "accuracy": 135.6,
                "altitude": 179.4,
                "latitude": 1.0,
                "longitude": 1.0,
            },
            {
                "sensor": "lamp.gps",
                "timestamp": 20,
                "accuracy": 135.6,
                "altitude": 179.4,
                "latitude": 2.0,
                "longitude": 2.0,
            },
            {
                "sensor": "lamp.gps",
                "timestamp": 25,
                "accuracy": 135.6,
                "altitude": 179.4,
                "latitude": 2.0,
                "longitude": 2.0,
            },
        ]
        sig = primary.significant_locations(gps_events, start=0, end=30)
        self.assertEqual(len(sig["data"]), 2)
        self.assertEqual(sig["data"][0]["duration"], 20)
        ht = secondary.hometime(gps_events, start=0, end=30)
        self.assertEqual(ht["value"], 20)
        ent = secondary.entropy(gps_events, start=0, end=30)
        import math
        self.assertTrue(math.isclose(ent["value"], 0.6365141682948128, rel_tol=1e-6))


if __name__ == "__main__":
    unittest.main()
