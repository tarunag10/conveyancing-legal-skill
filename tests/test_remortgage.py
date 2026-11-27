import json
import unittest
from copy import deepcopy
from pathlib import Path

from conveyancing_skill.remortgage import ReconciliationError, reconcile_remortgage

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "remortgage-reconciliation-synthetic.json"


class RemortgageReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.matter = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_synthetic_multi_security_reconciliation_and_human_blockers(self):
        result = reconcile_remortgage(self.matter)
        self.assertEqual("125000.00", result["gross_advance"])
        self.assertEqual("2000.00", result["itemised_lender_deductions"])
        self.assertEqual("123000.00", result["calculated_net_advance"])
        self.assertEqual("105000.00", result["redemption_total_included"])
        self.assertEqual("240.00", result["additional_vat"])
        self.assertEqual("106520.00", result["total_payments"])
        self.assertEqual("-21480.00", result["signed_balance_payments_less_receipts"])
        self.assertEqual("21480.00", result["balance"])
        self.assertEqual("Balance potentially refundable to client", result["balance_label"])
        self.assertFalse(result["ready_to_issue_or_release"])
        self.assertTrue(any("expected, not confirmed cleared" in x for x in result["blockers"]))

    def test_withheld_deduction_cannot_be_counted_again_as_payment(self):
        matter = deepcopy(self.matter)
        matter["payments"].append({"id":"repeat-arrangement","amount":"1500.00","vat_treatment":"not_applicable","included_deduction_id":"arrangement-fee","source_ref":"Synthetic","source_locator":"Line 4"})
        result = reconcile_remortgage(matter)
        self.assertTrue(any("Double-count risk" in x for x in result["blockers"]))

    def test_discrepant_confirmed_net_is_flagged_not_substituted(self):
        matter = deepcopy(self.matter)
        matter["advance"]["confirmed_net_amount"] = "122999.00"
        result = reconcile_remortgage(matter)
        self.assertEqual("123000.00", result["calculated_net_advance"])
        self.assertTrue(any("Net advance discrepancy" in x for x in result["blockers"]))

    def test_unrelated_security_is_excluded_and_flagged(self):
        matter = deepcopy(self.matter)
        matter["redemptions"].append({"id":"unrelated","security_id":"SEC-OTHER","quoted_amount":"2500.00","quoted_date":"2026-11-27","valid_until":"2026-11-27","source_ref":"Synthetic quote","source_locator":"Balance"})
        result = reconcile_remortgage(matter)
        self.assertEqual("105000.00", result["redemption_total_included"])
        self.assertTrue(any("not in the instructed security list" in x for x in result["blockers"]))

    def test_expired_redemption_is_excluded_and_flagged(self):
        matter = deepcopy(self.matter)
        matter["redemptions"][0]["valid_until"] = "2026-11-26"
        result = reconcile_remortgage(matter)
        self.assertEqual("30000.00", result["redemption_total_included"])
        self.assertEqual("expired_or_out_of_period", result["redemptions"][0]["status"])
        self.assertTrue(any("fresh dated figure" in x for x in result["blockers"]))
        self.assertIsNone(result["balance"])
        self.assertEqual("Unresolved; confirm financial inputs", result["balance_label"])

    def test_vat_mismatch_is_flagged_and_invalid_classification_rejected(self):
        matter = deepcopy(self.matter)
        matter["invoice_vat"] = "241.00"
        result = reconcile_remortgage(matter)
        self.assertTrue(any("VAT discrepancy" in x for x in result["blockers"]))
        matter["payments"][1]["vat_treatment"] = "not_applicable"
        matter["payments"][1]["vat_rate"] = "0.20"
        with self.assertRaises(ReconciliationError):
            reconcile_remortgage(matter)

    def test_financial_line_requires_document_and_locator(self):
        matter = deepcopy(self.matter)
        del matter["payments"][0]["source_locator"]
        with self.assertRaisesRegex(ReconciliationError, "source_ref and source_locator"):
            reconcile_remortgage(matter)

    def test_intended_security_requires_register_evidence(self):
        matter = deepcopy(self.matter)
        del matter["intended_securities"][0]["source_locator"]
        with self.assertRaisesRegex(ReconciliationError, "source_ref and source_locator"):
            reconcile_remortgage(matter)

    def test_redemption_quote_for_another_date_is_not_daily_rate_guessed(self):
        matter = deepcopy(self.matter)
        matter["redemptions"][0]["quoted_date"] = "2026-11-26"
        result = reconcile_remortgage(matter)
        self.assertEqual("date_mismatch", result["redemptions"][0]["status"])
        self.assertEqual("30000.00", result["redemption_total_included"])


if __name__ == "__main__":
    unittest.main()
