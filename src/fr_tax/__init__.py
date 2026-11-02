"""French Bandwidth Tax (PLF Amendment I-1358) calculation engine for autonomous agents."""

from .models import (
    DataUnit,
    TaxAssessmentInput,
    TaxAssessmentResult,
    TrafficOriginType,
    ISPTelemetryRecord,
    OptimizationDecision,
)
from .core import (
    TAX_RATE_PER_GB,
    CAP_FRANCE_REVENUE_RATIO,
    CAP_GLOBAL_REVENUE_RATIO,
    to_gigabytes,
    compute_statutory_caps,
    evaluate_data_tax,
)
from .calendar import get_compliance_deadlines
from .decision_engine import evaluate_payload_economics
from .tools import (
    calculate_french_data_tax,
    simulate_streaming_workload,
    assess_distribution_economics,
)

__all__ = [
    "DataUnit",
    "TaxAssessmentInput",
    "TaxAssessmentResult",
    "TrafficOriginType",
    "ISPTelemetryRecord",
    "OptimizationDecision",
    "TAX_RATE_PER_GB",
    "CAP_FRANCE_REVENUE_RATIO",
    "CAP_GLOBAL_REVENUE_RATIO",
    "to_gigabytes",
    "compute_statutory_caps",
    "evaluate_data_tax",
    "get_compliance_deadlines",
    "evaluate_payload_economics",
    "calculate_french_data_tax",
    "simulate_streaming_workload",
    "assess_distribution_economics",
]
