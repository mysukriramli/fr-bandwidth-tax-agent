from decimal import Decimal, ROUND_HALF_UP
from .models import OptimizationDecision

TAX_RATE_PER_GB = Decimal("0.055")


def evaluate_payload_economics(
    payload_size_gb: Decimal,
    revenue_per_unit_eur: Decimal,
    cdn_cost_per_gb_eur: Decimal = Decimal("0.005"),
    max_tolerated_margin_loss_pct: Decimal = Decimal("0.30"),
) -> OptimizationDecision:
    """
    Agent tool to evaluate if an asset (game, AI checkpoint, video stream)
    remains profitable under the €0.055/GB tax.
    """
    tax_eur = (payload_size_gb * TAX_RATE_PER_GB).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    delivery_cost_eur = (payload_size_gb * cdn_cost_per_gb_eur).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    total_variable_cost = delivery_cost_eur + tax_eur
    net_margin = revenue_per_unit_eur - total_variable_cost
    original_margin = revenue_per_unit_eur - delivery_cost_eur

    if net_margin <= Decimal("0.00"):
        return OptimizationDecision(
            action="geoblock_or_surcharge",
            gross_margin_eur=original_margin,
            tax_cost_eur=tax_eur,
            net_margin_after_tax=net_margin,
            warning=f"Tax (€{tax_eur}) exceeds commercial margin. Surcharge or traffic block recommended.",
        )

    margin_erosion = (tax_eur / original_margin) if original_margin > Decimal("0.00") else Decimal("1.0")

    if margin_erosion > max_tolerated_margin_loss_pct:
        reduction_target = (
            ((margin_erosion - max_tolerated_margin_loss_pct) / margin_erosion) * Decimal("100")
        ).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        return OptimizationDecision(
            action="transcode_reduce",
            gross_margin_eur=original_margin,
            tax_cost_eur=tax_eur,
            net_margin_after_tax=net_margin,
            recommended_bitrate_reduction_pct=reduction_target,
            warning=f"Tax erodes {margin_erosion * 100:.1f}% of margin. Compress file/bitrate by {reduction_target}%.",
        )

    return OptimizationDecision(
        action="absorb",
        gross_margin_eur=original_margin,
        tax_cost_eur=tax_eur,
        net_margin_after_tax=net_margin,
        warning=None,
    )
