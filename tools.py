from datetime import datetime

from data import MERCHANTS, TRANSACTIONS


# =========================================================
# MERCHANT
# =========================================================

def get_merchant(merchant_id):
    """Return merchant information by ID."""

    for merchant in MERCHANTS:
        if merchant["id"] == merchant_id:
            return merchant

    return None


# =========================================================
# TRANSACTIONS
# =========================================================

def get_merchant_transactions(merchant_id):
    """Return all transactions belonging to a merchant."""

    return [
        tx
        for tx in TRANSACTIONS
        if tx["merchant"] == merchant_id
    ]


def get_customer_transactions(customer_id):
    """Return all transactions belonging to a customer."""

    return [
        tx
        for tx in TRANSACTIONS
        if tx["customer"] == customer_id
    ]


# =========================================================
# DETECTOR 1 — DUPLICATE PAYMENTS
# =========================================================

def detect_duplicate_payments(merchant_id):
    """Detect suspicious duplicate successful payments."""

    transactions = get_merchant_transactions(merchant_id)

    leaks = []

    for i, tx1 in enumerate(transactions):

        for tx2 in transactions[i + 1:]:

            same_customer = tx1["customer"] == tx2["customer"]
            same_amount = tx1["amount"] == tx2["amount"]

            both_successful = (
                tx1["status"] == "success"
                and tx2["status"] == "success"
            )

            if same_customer and same_amount and both_successful:

                time1 = datetime.fromisoformat(tx1["timestamp"])
                time2 = datetime.fromisoformat(tx2["timestamp"])

                seconds = abs(
                    (time2 - time1).total_seconds()
                )

                if seconds <= 300:

                    leaks.append({
                        "type": "Duplicate Payment",
                        "merchant": merchant_id,
                        "customer": tx1["customer"],
                        "amount": tx2["amount"],
                        "transaction": tx2["id"],
                        "confidence": 94,
                        "severity": "HIGH",
                        "evidence": (
                            f"Two successful payments of "
                            f"₹{tx1['amount']:,} were made "
                            f"{int(seconds)} seconds apart."
                        ),
                    })

    return leaks


# =========================================================
# DETECTOR 2 — FAILED RENEWALS
# =========================================================

def detect_failed_renewals(merchant_id):
    """Detect failed subscription renewal payments."""

    transactions = get_merchant_transactions(merchant_id)

    leaks = []

    for tx in transactions:

        if (
            tx["status"] == "failed"
            and tx["type"] == "subscription_renewal"
        ):

            leaks.append({
                "type": "Failed Renewal",
                "merchant": merchant_id,
                "customer": tx["customer"],
                "amount": tx["amount"],
                "transaction": tx["id"],
                "confidence": 88,
                "severity": "MEDIUM",
                "evidence": (
                    "A subscription renewal payment failed "
                    "and may be recoverable."
                ),
            })

    return leaks


# =========================================================
# DETECTOR 3 — ABANDONED PAYMENTS
# =========================================================

def detect_abandoned_payments(merchant_id):
    """Detect payments that were started but abandoned."""

    transactions = get_merchant_transactions(merchant_id)

    leaks = []

    for tx in transactions:

        if tx["status"] == "abandoned":

            leaks.append({
                "type": "Abandoned Payment",
                "merchant": merchant_id,
                "customer": tx["customer"],
                "amount": tx["amount"],
                "transaction": tx["id"],
                "confidence": 79,
                "severity": "LOW",
                "evidence": (
                    "A payment was initiated but "
                    "was never completed."
                ),
            })

    return leaks


# =========================================================
# DETECTOR 4 — DUPLICATE REFUNDS
# =========================================================

def detect_duplicate_refunds(merchant_id):
    """Detect multiple refunds issued to the same customer."""

    transactions = get_merchant_transactions(merchant_id)

    leaks = []

    for i, tx1 in enumerate(transactions):

        for tx2 in transactions[i + 1:]:

            same_customer = tx1["customer"] == tx2["customer"]

            both_refunded = (
                tx1["status"] == "refunded"
                and tx2["status"] == "refunded"
            )

            if same_customer and both_refunded:

                leaks.append({
                    "type": "Duplicate Refund",
                    "merchant": merchant_id,
                    "customer": tx1["customer"],
                    "amount": tx2["amount"],
                    "transaction": tx2["id"],
                    "confidence": 91,
                    "severity": "HIGH",
                    "evidence": (
                        "Multiple refunds were issued "
                        "for the same customer."
                    ),
                })

    return leaks


# =========================================================
# MAIN SCANNER
# =========================================================

def scan_for_leaks(merchant_id):
    """
    Run every detection rule for ONE merchant.
    """

    leaks = []

    leaks.extend(
        detect_duplicate_payments(merchant_id)
    )

    leaks.extend(
        detect_failed_renewals(merchant_id)
    )

    leaks.extend(
        detect_abandoned_payments(merchant_id)
    )

    leaks.extend(
        detect_duplicate_refunds(merchant_id)
    )

    # Give every leak a unique ID for this merchant.
    for index, leak in enumerate(leaks, start=1):
        leak["id"] = f"{merchant_id}-LEAK-{index:03}"

    return leaks


# =========================================================
# INVESTIGATION DATA
# =========================================================

def investigate_leak(leak_id, merchant_id):
    """
    Gather all evidence required by the AI agent.
    """

    leaks = scan_for_leaks(merchant_id)

    selected_leak = None

    for leak in leaks:

        if leak["id"] == leak_id:
            selected_leak = leak
            break

    if selected_leak is None:
        return None

    merchant = get_merchant(
        selected_leak["merchant"]
    )

    customer_history = get_customer_transactions(
        selected_leak["customer"]
    )

    return {
        "leak": selected_leak,
        "merchant": merchant,
        "customer_history": customer_history,
    }