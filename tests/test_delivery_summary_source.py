import unittest

from src.ticket_workflow_seed import delivery_summary


class DeliverySummarySourceTests(unittest.TestCase):
    def test_default_shape_is_unchanged(self):
        summary = delivery_summary({"owner": "ops", "status": "queued", "source": "csv"})
        self.assertEqual(summary, {"owner": "ops", "status": "queued"})

    def test_opt_in_adds_source_field(self):
        summary = delivery_summary(
            {"owner": "ops", "status": "queued", "source": "csv"},
            include_source=True,
        )
        self.assertEqual(summary, {"owner": "ops", "status": "queued", "source": "csv"})

    def test_opt_in_source_is_trimmed(self):
        summary = delivery_summary(
            {"owner": "ops", "status": "queued", "source": " csv "},
            include_source=True,
        )
        self.assertEqual(summary["source"], "csv")

    def test_missing_source_reports_unknown(self):
        summary = delivery_summary({"owner": "ops", "status": "queued"}, include_source=True)
        self.assertEqual(summary["source"], "unknown")

    def test_blank_source_reports_unknown(self):
        summary = delivery_summary(
            {"owner": "ops", "status": "queued", "source": "   "},
            include_source=True,
        )
        self.assertEqual(summary["source"], "unknown")

    def test_input_record_is_not_mutated(self):
        record = {"owner": "ops", "status": "queued"}
        delivery_summary(record, include_source=True)
        self.assertEqual(record, {"owner": "ops", "status": "queued"})


if __name__ == "__main__":
    unittest.main()
