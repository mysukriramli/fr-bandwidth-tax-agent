from decimal import Decimal
from datetime import date
from fr_tax.core import evaluate_data_tax
from fr_tax.models import DataUnit
from fr_tax.calendar import get_compliance_deadlines
from fr_tax.decision_engine import evaluate_payload_economics
from fr_tax.tools import calculate_french_data_tax, simulate_streaming_workload


def test_single_game_download():
    res = evaluate_data_tax(volume=Decimal("150"), unit=DataUnit.GIGABYTES)
    assert res.raw_tax_eur == Decimal("8.25")
    assert res.effective_tax_eur == Decimal("8.25")
    assert res.cap_applied is None


def test_15_percent_french_turnover_cap():
    res = evaluate_data_tax(
        volume=Decimal("1"),
        unit=DataUnit.PETABYTES,
        turnover_fr=Decimal("100000.00"),
    )
    assert res.raw_tax_eur == Decimal("55000.00")
    assert res.effective_tax_eur == Decimal("15000.00")
    assert res.cap_applied == "15%_french_turnover"


def test_2_percent_global_turnover_cap():
    res = evaluate_data_tax(
        volume=Decimal("1000"),
        unit=DataUnit.TERABYTES,
        turnover_fr=Decimal("200000.00"),
        turnover_global=Decimal("500000.00"),
    )
    assert res.effective_tax_eur == Decimal("10000.00")
    assert res.cap_applied == "2%_global_turnover"


def test_videolan_nonprofit_scenario():
    res = evaluate_data_tax(volume=Decimal("800"), unit=DataUnit.TERABYTES)
    assert res.effective_tax_eur == Decimal("44000.00")


def test_compliance_deadlines():
    deadlines = get_compliance_deadlines(2026)
    assert deadlines["assessment_notice_deadline"] == date(2027, 1, 30)
    assert deadlines["tax_settlement_deadline"] == date(2027, 3, 30)


def test_decision_engine_unprofitable_payload():
    decision = evaluate_payload_economics(
        payload_size_gb=Decimal("500"),
        revenue_per_unit_eur=Decimal("10.00"),
    )
    assert decision.action == "geoblock_or_surcharge"
    assert decision.net_margin_after_tax < Decimal("0.00")


def test_decision_engine_transcode_mitigation():
    decision = evaluate_payload_economics(
        payload_size_gb=Decimal("100"),
        revenue_per_unit_eur=Decimal("12.00"),
        max_tolerated_margin_loss_pct=Decimal("0.30"),
    )
    assert decision.action == "transcode_reduce"
    assert decision.recommended_bitrate_reduction_pct is not None


def test_tools_wrapper_json_output():
    out = calculate_french_data_tax(volume=10.0, unit="GB")
    assert out["raw_tax_eur"] == "0.55"
    assert out["effective_tax_eur"] == "0.55"


def test_streaming_workload_simulation():
    res = simulate_streaming_workload(
        concurrent_users=1000,
        average_bitrate_mbps=5.0,
        hours_per_day=2.0,
        days=30,
    )
    assert "workload_summary" in res
    assert res["workload_summary"]["raw_tax_liability_eur"] > 0
