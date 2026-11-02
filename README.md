# fr-bandwidth-tax-agent

Deterministic computation, simulation, and audit engine designed for autonomous agents evaluating liability under France's proposed €0.055/GB digital data tax (PLF Amendment n°I-1358, Articles 302 bis ZP–ZS).

## Features
- **Deterministic Precision**: Full `decimal.Decimal` computation to avoid floating-point drift in statutory audits.
- **Statutory Cap Modeling**: Enforces dual caps (lesser of 15% French turnover or 2% global turnover).
- **DGFiP Deadlines**: Tracks Article 302 bis ZR filing and settlement schedules.
- **FinOps Decision Engine**: Recommends payload-level actions (`absorb`, `transcode_reduce`, `geoblock_or_surcharge`).
- **Agent Schemas**: Pre-configured OpenAI and LangChain JSON function-calling definitions.

## Installation
```bash
pip install -e .
