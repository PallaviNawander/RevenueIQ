
import json
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

from tools import investigate_leak


# =========================================================
# API KEY
# =========================================================

load_dotenv()

# Local development:
# GEMINI_API_KEY comes from .env
#
# Streamlit Cloud:
# GEMINI_API_KEY comes from Streamlit Secrets

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Add it to .env locally or to "
        "Streamlit Cloud → Settings → Secrets."
    )


client = genai.Client(
    api_key=api_key
)


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are RevenueIQ, an expert AI revenue recovery investigator.

You investigate suspected revenue leaks for merchants.

The detection system has already identified a potential leak.

Your job is to investigate the evidence and determine:

1. What happened?
2. Why is it likely a revenue leak?
3. What evidence proves it?
4. How confident are you?
5. What is the financial risk?
6. What recovery action should be taken?
7. How much revenue can potentially be recovered?

STRICT RULES:

- Use ONLY the evidence provided.
- Never invent transaction IDs.
- Never invent customers.
- Never invent amounts.
- Never invent dates.
- Never claim something happened if it is not supported by evidence.
- If evidence is insufficient, say so.
- Do not recommend a refund unless the evidence supports a refund.
- Do not recommend recovering more money than the transaction amount provided.

Possible actions:

REFUND
RETRY_PAYMENT
CONTACT_CUSTOMER
IGNORE
ESCALATE

Return ONLY valid JSON.

Use exactly this structure:

{
    "summary": "Short one sentence summary",
    "finding": "Detailed explanation of what happened",
    "evidence": [
        "Evidence point 1",
        "Evidence point 2",
        "Evidence point 3"
    ],
    "confidence": 0,
    "risk": "LOW",
    "recommended_action": "REFUND",
    "recovery_amount": 0,
    "reason": "Why this action is appropriate"
}

confidence must be an integer between 0 and 100.

risk must be exactly one of:

LOW
MEDIUM
HIGH
"""


# =========================================================
# INVESTIGATION
# =========================================================

def investigate(leak_id, merchant_id):
    """Investigate a detected revenue leak using Gemini."""

    evidence = investigate_leak(
        leak_id,
        merchant_id
    )

    if evidence is None:
        return {
            "error": "Leak not found."
        }

    prompt = f"""
Investigate the following detected revenue leak.

This information comes from RevenueIQ's verified
transaction analysis tools.

DO NOT invent any additional information.

VERIFIED EVIDENCE:

{json.dumps(evidence, indent=2)}

Analyze the evidence carefully.

Return the investigation in the required JSON format.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0,
                "response_mime_type": "application/json",
            }
        )

        return json.loads(response.text)

    except Exception as e:

        return {
            "error": str(e)
        }


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    result = investigate(
        "M001-LEAK-001",
        "M001"
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )
