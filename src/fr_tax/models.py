from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class DataUnit(str, Enum):
    BYTES = "B"
    MEGABYTES = "MB"
    GIGABYTES = "GB"
    TERABYTES = "TB"
    PETABYTES = "PB"
    MEBIBYTES = "MiB"
    GIBIBYTES = "GiB"
    TEBIBYTES = "TiB"


class TrafficOriginType(str, Enum):
    DIRECT = "direct_origin"
    CDN_EGRESS = "cdn_egress"


class TaxAssessmentInput(BaseModel):
    volume: Decimal = Field(..., description="Data transfer volume")
    unit: DataUnit = Field(default=DataUnit.GIGABYTES, description="Unit of data volume")
    annual_turnover_fr: Optional[Decimal] = Field(
        None, description="Annual French turnover in EUR (subject to 15% cap)"
    )
    annual_turnover_global: Optional[Decimal] = Field(
        None, description="Annual Worldwide revenue in EUR (subject to 2% cap)"
    )
    subscribers_fr: Optional[int] = Field(
        None, description="French subscriber count to evaluate per-user pass-through"
    )


class TaxAssessmentResult(BaseModel):
    volume_gb: Decimal = Field(..., description="Normalized volume in standard GB (10^9 bytes)")
    statutory_rate_eur_per_gb: Decimal
    raw_tax_eur: Decimal = Field(..., description="Tax before statutory caps")
    cap_applied: Optional[str] = Field(None, description="None, '15%_french_turnover', or '2%_global_turnover'")
    effective_tax_eur: Decimal = Field(..., description="Final tax payable after caps")
    effective_rate_per_gb: Decimal
    cost_per_subscriber_eur: Optional[Decimal] = None


class ISPTelemetryRecord(BaseModel):
    """Corresponds to Article 302 bis ZR reporting requirements."""
    emitter_iana_asn: int = Field(..., description="IANA / AS Number of the data emitter")
    emitter_legal_name: str
    traffic_type: TrafficOriginType = TrafficOriginType.DIRECT
    quarter: int = Field(..., ge=1, le=4)
    reporting_year: int
    bytes_delivered: int = Field(..., description="Raw bytes delivered to French subscribers")


class OptimizationDecision(BaseModel):
    action: str = Field(..., description="'pass_through', 'transcode_reduce', 'geoblock_or_surcharge', 'absorb'")
    gross_margin_eur: Decimal
    tax_cost_eur: Decimal
    net_margin_after_tax: Decimal
    recommended_bitrate_reduction_pct: Optional[Decimal] = None
    warning: Optional[str] = None
