import unittest

from src.delivery_filters import filter_delivery_records


RECORDS = [
    {"owner": " Billing-Ops ", "status": "queued"},
    {"owner": "support", "status": "shipped"},
    {"owner": "BILLING-OPS", "status": "done"},
    {"owner": None, "status": "queued"},
]


class DeliveryFilterTests(unittest.TestCase):
    def test_none_selection_means_no_filtering(self):
        self.assertEqual(filter_delivery_records(RECORDS, None), RECORDS)

    def test_empty_selection_returns_no_records(self):
        self.assertEqual(filter_delivery_records(RECORDS, []), [])

    def test_matching_uses_canonical_owner_semantics(self):
        result = filter_delivery_records(RECORDS, ["billing-ops"])
        self.assertEqual(result, [RECORDS[0], RECORDS[2]])

    def test_input_order_is_preserved(self):
        result = filter_delivery_records(RECORDS, ["support", "Billing-Ops"])
        self.assertEqual(result, [RECORDS[0], RECORDS[1], RECORDS[2]])

    def test_blank_owner_matches_default_route(self):
        result = filter_delivery_records(RECORDS, ["engineering-ops"])
        self.assertEqual(result, [RECORDS[3]])


if __name__ == "__main__":
    unittest.main()
