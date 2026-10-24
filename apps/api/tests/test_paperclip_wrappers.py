import unittest
from unittest.mock import patch

from phoenix.tools import paperclip


class _Response:
    def __init__(self, output: str):
        self.output = output


class _StubClient:
    def __init__(self):
        self.last_ask_image_kwargs = None

    def sql(self, query, **kwargs):
        return _Response("ERR [exit 2] sql error: table does not exist")

    def lookup(self, field, value, **kwargs):
        raise RuntimeError(f"lookup failed for {field}={value}")

    def ask_image(self, path, **kwargs):
        self.last_ask_image_kwargs = kwargs
        return _Response("Figure read complete for NCT01327846.")


class PaperclipWrapperTests(unittest.TestCase):
    def test_search_returns_unavailable_without_sdk_or_key(self):
        with patch.object(paperclip, "available", return_value=False):
            out = paperclip.search("canakinumab target engagement", source="trials")

        self.assertEqual(out["operation"], "search")
        self.assertEqual(out["status"], "unavailable")
        self.assertIn("unavailable", out["error"])

    def test_sql_err_output_is_downgraded_to_error(self):
        client = _StubClient()
        with (
            patch.object(paperclip, "available", return_value=True),
            patch.object(paperclip, "_client", return_value=client),
        ):
            out = paperclip.sql("select * from trials", source="trials")

        self.assertEqual(out["operation"], "sql")
        self.assertEqual(out["status"], "error")
        self.assertEqual(out["output"], "")
        self.assertIn("ERR", out["error"])

    def test_lookup_exception_returns_error_payload(self):
        client = _StubClient()
        with (
            patch.object(paperclip, "available", return_value=True),
            patch.object(paperclip, "_client", return_value=client),
        ):
            out = paperclip.lookup("doi", "10.1000/example")

        self.assertEqual(out["operation"], "lookup")
        self.assertEqual(out["status"], "error")
        self.assertIn("lookup failed", out["error"])
        self.assertEqual(out["field"], "doi")

    def test_ask_image_passes_question_through(self):
        client = _StubClient()
        with (
            patch.object(paperclip, "available", return_value=True),
            patch.object(paperclip, "_client", return_value=client),
        ):
            out = paperclip.ask_image(
                "papers/tri_abc123/figures/1.png",
                question="Did the PD biomarker move?",
            )

        self.assertEqual(out["operation"], "ask_image")
        self.assertEqual(out["status"], "ok")
        self.assertIn("NCT01327846", out["output"])
        self.assertEqual(
            client.last_ask_image_kwargs["question"],
            "Did the PD biomarker move?",
        )


if __name__ == "__main__":
    unittest.main()
