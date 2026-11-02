from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Tuple
from .models import DataUnit, TaxAssessmentResult

TAX_RATE_PER_GB = Decimal("0.055")
CAP_FRANCE_REVENUE_RATIO = Decimal("0.15")
CAP_GLOBAL_REVENUE_RATIO = Decimal("0.02")

UNIT_MULTIPLIERS = {
    DataUnit.BYTES: Decimal("1") / Decimal("1000000000"),
    DataUnit.MEGABYTES: Decimal("0.001"),
    DataUnit.GIGABYTES: Decimal("1.0"),
    DataUnit.TERABYTES: Decimal("1000.0"),
    DataUnit.PETABYTES: Decimal("1000000.0"),
    DataUnit.MEBIBYTES: (Decimal("1024") ** 2) / Decimal("1000000000"),
    DataUnit.GIBIBYTES: (Decimal("1024") ** 3) / Decimal("1000000000"),
    DataUnit.TEBIBYTES: (Decimal("1024") ** 4) / Decimal("1000000000"),
}


def to_gigabytes(volume: Decimal, unit: DataUnit) -> Decimal:
    """Converts any data volume to standard gigabytes (1 GB = 10^9 B)."""
    return (volume * UNIT_MULTIPLIERS[unit]).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def compute_statutory_caps(
    raw_tax: Decimal,
    turnover_fr: Optional[Decimal],
    turnover_global: Optional[Decimal],
) -> Tuple[Decimal, Optional[str]]:
    """Evaluates the 15% French revenue cap and 2% global revenue cap."""
    effective_tax = raw_tax
    cap_applied = None

    cap_fr = turnover_fr * CAP_FRANCE_REVENUE_RATIO if turnover_fr is not None else None
    cap_glob = turnover_global * CAP_GLOBAL_REVENUE_RATIO if turnover_global is not None else None

    candidates = [(effective_tax, None)]
    if cap_fr is not None:
        candidates.append((cap_fr, "15%_french_turnover"))
    if cap_glob is not None:
        candidates.append((cap_glob, "2%_global_turnover"))

    effective_tax, cap_applied = min(candidates, key=lambda x: x[0])

    if effective_tax >= raw_tax:
        return raw_tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), None

    return effective_tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), cap_applied


def evaluate_data_tax(
    volume: Decimal,
    unit: DataUnit = DataUnit.GIGABYTES,
    turnover_fr: Optional[Decimal] = None,
    turnover_global: Optional[Decimal] = None,
    subscribers_fr: Optional[int] = None,
) -> TaxAssessmentResult:
    """Primary calculation routine for agent execution."""
    volume_gb = to_gigabytes(volume, unit)
    raw_tax = (volume_gb * TAX_RATE_PER_GB).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    effective_tax, cap_applied = compute_statutory_caps(raw_tax, turnover_fr, turnover_global)
    
    effective_rate = (
        (effective_tax / volume_gb).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
        if volume_gb > 0 else Decimal("0.00")
    )
    
    cost_per_sub = None
    if subscribers_fr and subscribers_fr > 0:
        cost_per_sub = (effective_tax / Decimal(subscribers_fr)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return TaxAssessmentResult(
        volume_gb=volume_gb,
        statutory_rate_eur_per_gb=TAX_RATE_PER_GB,
        raw_tax_eur=raw_tax,
        cap_applied=cap_applied,
        effective_tax_eur=effective_tax,
        effective_rate_per_gb=effective_rate,
        cost_per_subscriber_eur=cost_per_sub,
    )
