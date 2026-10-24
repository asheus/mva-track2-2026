"""ToolUniverse wrapper tests — degrade-safe behaviour, no network/SDK needed.

The live `run()` proxies remote APIs, so it is exercised by the calibration CLI, not here.
These pin the contract that matters for the demo: the wrapper NEVER raises, signals
unavailability cleanly, round-trips its on-disk cache, and detects error payloads.
"""
import os
import unittest
from unittest.mock import patch

from phoenix.tools import tooluniverse as tu


class DegradeSafeTest(unittest.TestCase):
    def test_kill_switch_returns_unavailable(self):
        with patch.dict(os.environ, {"PHOENIX_DISABLE_TOOLUNIVERSE": "1"}):
            r = tu.run("OpenTargets_get_drug_chembId_by_generic_name",
                       {"drugName": "canakinumab"}, use_cache=False)
        self.assertEqual(r["status"], "unavailable")
        self.assertEqual(r["name"], "OpenTargets_get_drug_chembId_by_generic_name")

    def test_run_never_raises_on_bad_load(self):
        # Force the registry load to fail; run() must degrade, not raise.
        with patch.object(tu, "_get_tu", return_value=None):
            r = tu.run("AnyTool", {"x": 1}, use_cache=False)
        self.assertEqual(r["status"], "unavailable")

    def test_cache_round_trip(self):
        name, args = "FakeTool_for_test", {"q": "z"}
        rec = {"name": name, "arguments": args, "status": "ok", "output": {"value": 42}}
        tu._write_cache(name, args, rec)
        try:
            got = tu.run(name, args)  # should hit cache, never touch the network
            self.assertEqual(got["status"], "ok")
            self.assertEqual(got["output"], {"value": 42})
            self.assertTrue(got["cached"])
        finally:
            tu._cache_path(name, args).unlink(missing_ok=True)


class ErrorDetectionTest(unittest.TestCase):
    def test_looks_like_error(self):
        self.assertIsNone(tu._looks_like_error({"status": "success", "data": {}}))
        self.assertIsNone(tu._looks_like_error([{"id": "x"}]))
        self.assertTrue(tu._looks_like_error({"error": "drug not found"}))
        self.assertTrue(tu._looks_like_error("ERROR: bad request"))
        self.assertTrue(tu._looks_like_error(None))


if __name__ == "__main__":
    unittest.main()
