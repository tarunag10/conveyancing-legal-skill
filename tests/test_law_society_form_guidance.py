"""Regression checks for the scoped Law Society TA form guidance record."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class LawSocietyFormGuidanceTests(unittest.TestCase):
    def test_rule_has_exact_transition_and_no_legal_approval(self):
        rule = next(x for x in load("knowledge/legislation/rules.json") if x["id"] == "r-law-society-ta6")
        self.assertEqual("2026-11-27", rule["last_verified_date"])
        self.assertFalse(rule["legal_reviewer_approved"])
        self.assertIn("already been used", rule["transitional_or_scope_note"])
        self.assertIn("not new-build", rule["transitional_or_scope_note"])
        self.assertIn("auctions", rule["transitional_or_scope_note"])

    def test_catalogue_distinguishes_guidance_from_binary_review(self):
        forms = {x["code"]: x for x in load("knowledge/forms/catalogue.json")}
        ta6, ta7 = forms["TA6"], forms["TA7"]
        self.assertEqual("2026-11-27", ta6["publisher_date_last_checked"])
        self.assertFalse(ta6["file_revision_verified"])
        self.assertFalse(ta7["file_revision_verified"])
        self.assertIn("not intended for new-build", ta6["purpose"])
        self.assertIn("auction", ta6["purpose"])
        self.assertEqual("https://www.lawsociety.org.uk/topics/property/ta6-6th-edition", ta6["official_form_page_url"])

    def test_practice_modules_preserve_new_build_and_auction_limits(self):
        auction = (ROOT / "knowledge/practice/AUCTIONS.md").read_text(encoding="utf-8").lower()
        development = (ROOT / "knowledge/practice/DEVELOPMENT_AND_SPECIAL.md").read_text(encoding="utf-8").lower()
        leasehold = (ROOT / "knowledge/practice/LEASEHOLD_AND_BUILDING_SAFETY.md").read_text(encoding="utf-8").lower()
        self.assertIn("may not be suitable for an auction", auction)
        self.assertIn("not intended for new-build purchases", development)
        self.assertIn("already been used", leasehold)

    def test_verification_record_keeps_review_gates_and_evidence_gaps(self):
        record = (ROOT / "docs/source-verification/2026-11-27-law-society-ta-forms.md").read_text(encoding="utf-8")
        for phrase in ["http 403", "not legal approval", "binaries were not inspected", "issues #7 and #8 open", "not intended for new-build"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, record.lower())


if __name__ == "__main__":
    unittest.main()
