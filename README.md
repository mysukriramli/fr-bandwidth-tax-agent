# fr-bandwidth-tax-agent

[![CI](https://github.com/mysukriramli/fr-bandwidth-tax-agent/actions/workflows/run_tax_audit.yml/badge.svg)](https://github.com/mysukriramli/fr-bandwidth-tax-agent/actions/workflows/run_tax_audit.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A deterministic computation, simulation, and audit engine designed for autonomous AI agents, CDN controllers, and FinOps platforms evaluating exposure under France's proposed digital bandwidth tax (**PLF Amendment n°I-1358**, Articles 302 *bis* ZP through 302 *bis* ZS).

---

## Overview

French parliamentary amendment n°I-1358 introduces a statutory levy of **€0.055 per Gigabyte (10⁹ bytes)** delivered over domestic access networks. 

This repository provides zero-drift financial computation, statutory turnover cap enforcement, DGFiP tax administration timelines, and an automated decision matrix that enables autonomous agents to select mitigation actions (`absorb`, `transcode_reduce`, `geoblock_or_surcharge`) prior to asset egress.

---

## Key Capabilities

* **Zero-Drift Deterministic Math**: Computes all base units, multipliers, tax levies, and effective rates exclusively via Python's standard `decimal.Decimal` (`ROUND_HALF_UP`) to prevent binary floating-point roundoff errors during statutory audits.
* **Dual Statutory Turnover Caps (Art. 302 *bis* ZQ)**: Enforces statutory ceiling criteria—capping total liability at the lesser of **15% of annual French turnover** or **2% of annual worldwide turnover**.
* **Statutory Compliance Calendar (Art. 302 *bis* ZR)**: Computes quarterly ISP telemetry declaration dates, DGFiP assessment notices (January 30 of Year $N+1$), and mandatory settlement deadlines (March 30 of Year $N+1$).
* **FinOps Decision Engine**: Evaluates delivery economics for digital assets (game patches, video streams, open-weight AI models) against delivery margins to recommend payload-level mitigations.
* **Agent Native**: Pre-built function-calling schemas formatted for OpenAI, LangChain, AutoGen, and CrewAI frameworks.

---

## Statutory Tax Framework

$$\text{Tax Base (GB)} = \frac{\text{Bytes Delivered}}{10^9}$$

$$\text{Raw Tax Liability} = \text{Tax Base (GB)} \times 0.055\ \text{EUR}$$

$$\text{Statutory Liability} = \min\Big(\text{Raw Tax},\ 0.15 \times \text{Turnover}_{\text{FR}},\ 0.02 \times \text{Turnover}_{\text{Global}}\Big)$$

---

## Repository Structure

```text
fr-bandwidth-tax-agent/
├── .github/
│   └── workflows/
│       └── run_tax_audit.yml      # Automated test suite & scenario runner
├── schemas/
│   └── agent_tools.json          # Pre-built OpenAI function-calling tools schema
├── src/
│   └── fr_tax/
│       ├── __init__.py           # Package exports
│       ├── calendar.py           # DGFiP filing & settlement schedule generator
│       ├── core.py               # Deterministic Decimal engine & statutory cap logic
│       ├── decision_engine.py    # Unit economics & mitigation decision tree
│       ├── models.py             # Pydantic v2 validation models & data contracts
│       └── tools.py              # Zero-drift tool interfaces for agent runtime
├── tests/
│   └── test_tax_engine.py       # Full statutory validation test suite
├── pyproject.toml                # Packaging & Hatchling build definition
├── run_simulation.py             # Headless CLI scenario simulation script
└── README.md
