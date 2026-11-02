from datetime import date
from typing import Dict


def get_compliance_deadlines(tax_year: int) -> Dict[str, date]:
    """
    Computes statutory DGFiP administrative deadlines (Art. 302 bis ZR):
    - Assessment notice issued by DGFiP: January 30, N+1
    - Mandatory tax settlement deadline: March 30, N+1
    """
    return {
        "q1_isp_submission": date(tax_year, 4, 30),
        "q2_isp_submission": date(tax_year, 7, 31),
        "q3_isp_submission": date(tax_year, 10, 31),
        "q4_isp_submission": date(tax_year + 1, 1, 31),
        "assessment_notice_deadline": date(tax_year + 1, 1, 30),
        "tax_settlement_deadline": date(tax_year + 1, 3, 30),
    }
