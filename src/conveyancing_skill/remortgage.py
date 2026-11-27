"""Evidence-gated remortgage funds reconciliation.

Arithmetic only. It neither verifies documents nor authorises a payment or completion.
Each financial input must carry a documentary reference and locator.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

PENNY = Decimal("0.01")
ZERO = Decimal("0.00")
VAT_TREATMENTS = {"net_taxable", "gross_inclusive", "true_disbursement", "exempt", "not_applicable"}


class ReconciliationError(ValueError):
    """Malformed input that cannot safely be reconciled."""


def _money(value, label="amount") -> Decimal:
    if isinstance(value, bool):
        raise ReconciliationError(f"{label}: boolean is not a monetary amount")
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ReconciliationError(f"{label}: invalid monetary amount") from exc
    if not amount.is_finite() or amount < ZERO or amount != amount.quantize(PENNY):
        raise ReconciliationError(f"{label}: amount must be nonnegative GBP with at most two decimal places")
    return amount.quantize(PENNY)


def _evidence(item, label):
    ref = item.get("source_ref")
    locator = item.get("source_locator")
    if not isinstance(ref, str) or not ref.strip() or not isinstance(locator, str) or not locator.strip():
        raise ReconciliationError(f"{label}: documentary source_ref and source_locator are required")
    return f"{ref.strip()} — {locator.strip()}"


def _date(value, label):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ReconciliationError(f"{label}: use an ISO date (YYYY-MM-DD)") from exc


def _rows(items, label):
    if not isinstance(items, list):
        raise ReconciliationError(f"{label}: expected a list")
    ids = set()
    total = ZERO
    clean = []
    for row in items:
        if not isinstance(row, dict):
            raise ReconciliationError(f"{label}: each row must be an object")
        rid = row.get("id")
        if not isinstance(rid, str) or not rid.strip() or rid in ids:
            raise ReconciliationError(f"{label}: missing or duplicate line id")
        ids.add(rid)
        amount = _money(row.get("amount"), f"{label}.{rid}")
        evidence = _evidence(row, f"{label}.{rid}")
        total += amount
        clean.append((row, amount, evidence))
    return total, clean


def reconcile_remortgage(matter: dict) -> dict:
    """Reconcile an explicitly evidenced remortgage input object.

    Amounts excluded due to expired/mismatched security evidence are returned as
    unresolved, never silently replaced with estimates. Receipt balance is
    payments minus projected receipts: positive is payable by client; negative
    is potentially refundable, subject to human ledger review.
    """
    if not isinstance(matter, dict) or matter.get("transaction_type") != "remortgage":
        raise ReconciliationError("transaction_type must be remortgage")
    completion_date = _date(matter.get("completion_date"), "completion_date")
    blockers = list(matter.get("unresolved_items", []))
    financial_discrepancy = bool(blockers)

    advance = matter.get("advance")
    if not isinstance(advance, dict):
        raise ReconciliationError("advance details are required")
    gross = _money(advance.get("gross_amount"), "gross advance")
    _evidence(advance, "gross advance")
    deduction_total, deductions = _rows(advance.get("deductions", []), "advance.deductions")
    if deduction_total > gross:
        raise ReconciliationError("itemised lender deductions exceed gross advance")
    net = gross - deduction_total
    net_evidence = advance.get("net_source_ref")
    net_locator = advance.get("net_source_locator")
    if not net_evidence or not net_locator:
        blockers.append("Net advance: lender remittance or covering letter reference and locator missing")
        financial_discrepancy = True
    elif "confirmed_net_amount" in advance:
        confirmed_net = _money(advance["confirmed_net_amount"], "confirmed net advance")
        if net != confirmed_net:
            blockers.append(f"Net advance discrepancy: itemised deductions produce £{net:,.2f}; lender confirms £{confirmed_net:,.2f}")
            financial_discrepancy = True

    deduction_ids = {d.get("id") for d, _, _ in deductions}
    for row in matter.get("payments", []):
        if row.get("included_deduction_id") in deduction_ids:
            blockers.append(f"Double-count risk: payment {row.get('id', 'unknown')} repeats withheld lender deduction {row['included_deduction_id']}")
            financial_discrepancy = True

    securities = matter.get("intended_securities")
    if not isinstance(securities, list) or not securities:
        raise ReconciliationError("intended_securities must identify at least one security to redeem")
    security_ids = set()
    for security in securities:
        if not isinstance(security, dict) or not security.get("security_id"):
            raise ReconciliationError("Each intended security needs a security_id")
        if security["security_id"] in security_ids:
            raise ReconciliationError("Duplicate intended security_id")
        _evidence(security, f"intended security.{security['security_id']}")
        security_ids.add(security["security_id"])
    redemptions = matter.get("redemptions", [])
    if not isinstance(redemptions, list):
        raise ReconciliationError("redemptions must be a list")
    redemption_sum = ZERO
    accepted_redemptions = []
    seen_redemptions = set()
    for r in redemptions:
        if not isinstance(r, dict) or not r.get("id") or r["id"] in seen_redemptions:
            raise ReconciliationError("redemptions: missing or duplicate line id")
        seen_redemptions.add(r["id"])
        _evidence(r, f"redemption.{r['id']}")
        sid = r.get("security_id")
        if sid not in security_ids:
            blockers.append(f"Redemption {r['id']}: security {sid!r} is not in the instructed security list; amount excluded")
            financial_discrepancy = True
            accepted_redemptions.append({"id": r["id"], "amount": None, "status": "unresolved_security"})
            continue
        quoted = _money(r.get("quoted_amount"), f"redemption.{r['id']}")
        quoted_date = _date(r.get("quoted_date"), f"redemption.{r['id']}.quoted_date")
        valid_from = _date(r.get("valid_from", str(quoted_date)), f"redemption.{r['id']}.valid_from")
        valid_until = _date(r.get("valid_until"), f"redemption.{r['id']}.valid_until") if r.get("valid_until") else None
        if completion_date < valid_from or valid_until is None or completion_date > valid_until:
            blockers.append(f"Redemption {r['id']}: quote is not valid for completion date; obtain a fresh dated figure; amount excluded")
            financial_discrepancy = True
            accepted_redemptions.append({"id": r["id"], "amount": None, "status": "expired_or_out_of_period"})
            continue
        if quoted_date != completion_date:
            blockers.append(f"Redemption {r['id']}: quote date differs from completion date; lender-confirmed exact-date amount required; amount excluded")
            financial_discrepancy = True
            accepted_redemptions.append({"id": r["id"], "amount": None, "status": "date_mismatch"})
            continue
        redemption_sum += quoted
        accepted_redemptions.append({"id": r["id"], "security_id": sid, "amount": str(quoted), "status": "quoted_for_completion_date"})

    payment_total, payment_rows = _rows(matter.get("payments", []), "payments")
    vat_by_rate = {}
    payment_detail = []
    for row, amount, evidence in payment_rows:
        treatment = row.get("vat_treatment")
        if treatment not in VAT_TREATMENTS:
            raise ReconciliationError(f"payments.{row['id']}: explicit VAT treatment required")
        rate = ZERO
        if treatment == "net_taxable":
            rate = Decimal(str(row.get("vat_rate", "-1")))
            if not rate.is_finite() or rate < ZERO or rate > 1:
                raise ReconciliationError(f"payments.{row['id']}: valid evidenced VAT rate required")
            vat_by_rate[rate] = vat_by_rate.get(rate, ZERO) + amount
        elif "vat_rate" in row:
            raise ReconciliationError(f"payments.{row['id']}: VAT rate supplied for non-net-taxable treatment")
        payment_detail.append({"id": row["id"], "amount": str(amount), "vat_treatment": treatment, "source": evidence})

    vat = sum(((net_base * rate).quantize(PENNY, rounding=ROUND_HALF_UP) for rate, net_base in vat_by_rate.items()), ZERO)
    if "invoice_vat" in matter:
        invoice_vat = _money(matter["invoice_vat"], "invoice VAT")
        if invoice_vat != vat:
            blockers.append(f"VAT discrepancy: calculated £{vat:,.2f}; invoice records £{invoice_vat:,.2f}; resolve before issuing")
            financial_discrepancy = True

    funds_total, funds = _rows(matter.get("client_funds", []), "client_funds")
    cleared = ZERO
    forecast = net
    for row, amount, evidence in funds:
        status = row.get("status")
        if status not in {"cleared", "expected", "unverified"}:
            raise ReconciliationError(f"client_funds.{row['id']}: status must be cleared, expected or unverified")
        if status == "cleared":
            cleared += amount
            forecast += amount
        elif status == "expected" and row.get("include_in_forecast") is True:
            forecast += amount
            blockers.append(f"Client funds {row['id']}: expected only; verify cleared receipt")
        else:
            blockers.append(f"Client funds {row['id']}: {status} funds excluded from forecast")

    total_payments = payment_total + redemption_sum + vat
    balance = total_payments - forecast
    unresolved_balance = financial_discrepancy or any(x["status"] != "quoted_for_completion_date" for x in accepted_redemptions)
    if cleared + (net if advance.get("status") == "cleared" else ZERO) < total_payments:
        blockers.append("Cleared funds do not cover listed payments; confirm cashier ledger and actual lender receipt")
    if advance.get("status") not in {"cleared", "expected"}:
        blockers.append("Lender advance receipt status is missing or unverified")
    elif advance.get("status") == "expected":
        blockers.append("Lender advance is expected, not confirmed cleared")
    if matter.get("bank_details_verified_by_human") is not True:
        blockers.append("Payment bank details not independently verified by an authorised human")
    if matter.get("lender_conditions_satisfied_by_human") is not True:
        blockers.append("Lender conditions not confirmed satisfied by an authorised human")
    if matter.get("cashier_ledger_reconciled_by_human") is not True:
        blockers.append("Client ledger not reconciled by an authorised human")

    return {
        "matter_reference": matter.get("matter_reference", "UNSPECIFIED"),
        "completion_date": str(completion_date),
        "gross_advance": str(gross),
        "itemised_lender_deductions": str(deduction_total),
        "calculated_net_advance": str(net),
        "redemptions": accepted_redemptions,
        "redemption_total_included": str(redemption_sum),
        "payments_before_vat": str(payment_total + redemption_sum),
        "additional_vat": str(vat),
        "total_payments": str(total_payments),
        "cleared_client_funds": str(cleared),
        "cleared_receipts_including_advance": str(cleared + (net if advance.get("status") == "cleared" else ZERO)),
        "forecast_receipts": str(forecast),
        "balance": None if unresolved_balance else str(abs(balance)),
        "balance_label": "Unresolved; confirm financial inputs" if unresolved_balance else "Balance payable by client" if balance > ZERO else "Balance potentially refundable to client" if balance < ZERO else "No balance due",
        "signed_balance_payments_less_receipts": None if unresolved_balance else str(balance),
        "provisional_signed_balance_payments_less_receipts": str(balance),
        "blockers": blockers,
        "ready_to_issue_or_release": False,
        "warning": "Arithmetic and evidence-presence checks only. Source documents, tax/VAT treatment, lender requirements, cleared funds and authority require human verification. Never use this result alone to issue a payment instruction or release funds.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON remortgage reconciliation input")
    args = parser.parse_args(argv)
    matter = json.loads(Path(args.input).read_text(encoding="utf-8"))
    print(json.dumps(reconcile_remortgage(matter), indent=2))


if __name__ == "__main__":
    main()
