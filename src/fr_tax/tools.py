import json
from decimal import Decimal
from typing import Dict, Any, Optional
from .models import DataUnit
from .core import evaluate_data_tax
from .decision_engine import evaluate_payload_economics


def calculate_french_data_tax(
    volume: float,
    unit: str = "GB",
    turnover_fr: Optional[float] = None,
    turnover_global: Optional[float] = None,
    subscribers_fr: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Autonomous Agent Tool:
    Computes tax liability under French PLF Amendment I-1358 (€0.055/GB).
    Applies 15% French and 2% global turnover caps where applicable.
    """
    try:
        data_unit = DataUnit(unit)
    except ValueError:
        return {"error": f"Invalid unit '{unit}'. Use one of: {[u.value for u in DataUnit]}"}

    res = evaluate_data_tax(
        volume=Decimal(str(volume)),
        unit=data_unit,
        turnover_fr=Decimal(str(turnover_fr)) if turnover_fr is not None else None,
        turnover_global=Decimal(str(turnover_global)) if turnover_global is not None else None,
        subscribers_fr=subscribers_fr,
    )
    
    return json.loads(res.model_dump_json())


def simulate_streaming_workload(
    concurrent_users: int,
    average_bitrate_mbps: float,
    hours_per_day: float,
    days: int = 30,
) -> Dict[str, Any]:
    """
    Autonomous Agent Tool:
    Calculates bandwidth consumption and tax for live or on-demand video streaming workloads.
    """
    gb_per_hour_per_stream = (Decimal(str(average_bitrate_mbps)) * Decimal("3600")) / Decimal("8000")
    total_hours = Decimal(str(hours_per_day)) * Decimal(str(days))
    total_gb = gb_per_hour_per_stream * total_hours * Decimal(str(concurrent_users))
    
    tax_result = evaluate_data_tax(
        volume=total_gb,
        unit=DataUnit.GIGABYTES,
        subscribers_fr=concurrent_users,
    )
    
    return {
        "workload_summary": {
            "concurrent_users": concurrent_users,
            "average_bitrate_mbps": average_bitrate_mbps,
            "total_streamed_gb": float(tax_result.volume_gb),
            "raw_tax_liability_eur": float(tax_result.raw_tax_eur),
            "estimated_tax_per_active_user_eur": (
                float(tax_result.cost_per_subscriber_eur)
                if tax_result.cost_per_subscriber_eur is not None else None
            ),
        }
    }


def assess_distribution_economics(
    payload_gb: float,
    sale_price_eur: float,
    cdn_cost_per_gb: float = 0.005,
) -> Dict[str, Any]:
    """
    Autonomous Agent Tool:
    Determines whether a digital payload can be profitably delivered to France under the €0.055/GB tax.
    """
    decision = evaluate_payload_economics(
        payload_size_gb=Decimal(str(payload_gb)),
        revenue_per_unit_eur=Decimal(str(sale_price_eur)),
        cdn_cost_per_gb_eur=Decimal(str(cdn_cost_per_gb)),
    )
    return decision.model_dump()
