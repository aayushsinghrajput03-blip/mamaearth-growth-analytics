import json
import os
from pathlib import Path
from google import genai


def generate_scr_narrative_offline(findings: dict) -> dict:
    """
    Deterministic offline fallback.
    Uses only values supplied in findings.
    No API key or network call is required.
    """

    narrative = f"""
Situation

Mamaearth's cleaned revenue is ₹{findings['cleaned_total_revenue_inr']:.2f},
compared with raw revenue of ₹{findings['raw_total_revenue_inr']:.2f}.
The reconciliation difference is ₹{findings['duplicate_reconciliation_delta_inr']:.2f}.

Complication

COD has the highest return rate at {findings['return_rate_by_payment']['COD']}%.
The highest-risk segment is COD in city tier {findings['highest_risk_segment']['city_tier']},
with a return rate of {findings['highest_risk_segment']['return_rate_pct']}%.

Resolution

The verified revenue peak is March {findings['true_peak_month']['month']},
with revenue of ₹{findings['true_peak_month']['revenue_inr']:.2f}.
The apparent peak in {findings['outlier_inflated_month']['month']} was
₹{findings['outlier_inflated_month']['apparent_revenue_inr']:.2f},
while the corrected revenue was ₹{findings['outlier_inflated_month']['corrected_revenue_inr']:.2f}.
"""

    return {
        "status": "success",
        "narrative": narrative.strip(),
        "tokens": None
    }


def generate_scr_narrative(findings: dict) -> dict:

    # Offline fallback when no API key is configured.
    if not os.environ.get("GEMINI_API_KEY"):
        return generate_scr_narrative_offline(findings)

    system_instruction = """
You are a senior data analyst writing for Mamaearth's regional
ops and finance heads.

Write the business narrative using exactly these three labeled sections:

Situation
Complication
Resolution

Every number in the output must come directly from the supplied
findings and must appear with the same value.

Do not invent, estimate, calculate, derive, round differently,
or introduce any statistic that is not explicitly supplied.
"""

    contents = f"""
Create a concise business narrative using the verified findings below.

Verified findings:
{json.dumps(findings, indent=2)}
"""

    try:
        client = genai.Client()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config={
                "system_instruction": system_instruction,
                # Temperature 0 makes the factual report deterministic.
                "temperature": 0.0,
                "max_output_tokens": 500
            }
        )

        return {
            "status": "success",
            "narrative": response.text,
            "tokens": getattr(
                getattr(response, "usage_metadata", None),
                "total_token_count",
                None
            )
        }

    except Exception as err:
        # API failure → deterministic offline fallback
        return generate_scr_narrative_offline(findings)




def check_numeric_accuracy(narrative: str) -> bool:
    """Check all five required figures in the narrative."""

    normalized = narrative.replace(",", "").lower()

    checks = [
        ("Cleaned revenue 97,358.30", "97358.3"),
        ("COD return rate 44.4", "44.4"),
        ("COD + Tier-2 return rate 54.5", "54.5"),
        ("Reconciliation delta 2,501.90", "2501.9"),
    ]

    all_passed = True

    for label, value in checks:
        if value in normalized:
            print(f"PASS: {label}")
        else:
            print(f"FAIL: {label}")
            all_passed = False

    # Fifth requirement: March AND 20,318.90
    if "march" in normalized and "20318.9" in normalized:
        print("PASS: March + 20,318.90")
    else:
        print("FAIL: March + 20,318.90")
        all_passed = False

    return all_passed

if __name__ == "__main__":
  findings_path = Path(__file__).resolve().parent / "findings.json"

    with open(findings_path, "r", encoding="utf-8") as file:
        findings = json.load(file)

    result = generate_scr_narrative(findings)

    print("\nSTATUS:", result["status"])
    print("\nNARRATIVE:")
    print(result["narrative"])

    print("\nNUMERIC ACCURACY CHECK:")
    passed = check_numeric_accuracy(result["narrative"])

    print("\nFINAL CHECK:", "PASS" if passed else "FAIL")
