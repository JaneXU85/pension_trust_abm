# Trust Collapse Under Negative Spillover  
### An Agent-Based Model of Collaborative Governance in China's Personal Pension System

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  
[![Reproducible](https://img.shields.io/badge/reproducible-100%25-brightgreen)]()

This repository contains the source code, experimental data, and visualization scripts for the paper:  
**"Trust Collapse Under Negative Spillover: An Agent-Based Model of Collaborative Governance with Implications for China's Personal Pension System"**

> **Core Finding**: Even minimal negative spillover (≥15%) triggers total system collapse—participation drops to 0% regardless of initial trust.

---

## 📌 Overview

We model a broker-mediated personal pension system inspired by China’s Pillar III framework, where citizens voluntarily contribute based on institutional trust. Using agent-based modeling (ABM), we demonstrate that **localized trust breaches can propagate via negative spillover**, leading to systemic non-participation.

The model follows the **ODD protocol (Overview, Design concepts, Details)** and includes:
- Heterogeneous citizen agents with dynamic trust updating
- Broker agents subject to stochastic scandals
- A global spillover mechanism that updates trust across the entire population
- Endogenous participation decisions (contribute or withdraw)

---

## 🔬 Key Results

| Condition                | Final Trust | Participation Rate |
|--------------------------|-------------|--------------------|
| No spillover (`β = 0.0`) | = Initial   | 100%               |
| Partial/Full spillover (`β ≥ 0.5`) | 0.0         | 0%                 |

- **Critical threshold**: System collapses when spillover intensity **exceeds ~0.15**
- **Initial trust is irrelevant**: High initial trust (0.9) cannot prevent collapse under spillover
- **Early warning**: Trust declines before participation—enabling detection of "zombie contributors"

> These results highlight the **structural fragility** of voluntary pension systems.

---

## 📂 Repository Structure

├── agents.py # Citizen & Broker agent definitions
├── model.py # Main model: PensionTrustModel
├── run_extended_experiment.py # Full factorial experiment (270 runs)
├── plot_results.py # Generates publication-ready figures
├── extended_experiment_all_runs.csv # Raw experimental data (270 rows)
├── figures/ # Output plots (300 DPI PNG)
│ ├── fig1_participation_boxplot.png
│ ├── fig2_participation_heatmap.png
│ └── fig3_trust_vs_participation.png; fig4
├── requirements.txt # Python dependencies
└── README.md # This file

---

## ▶️ How to Reproduce

### Prerequisites
- Python ≥ 3.8
- Git

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/trust_abm.git
   cd trust_abm



2.Install dependencies
pip install -r requirements.txt

3.Run the full experiment (takes ~2 minutes):
python run_extended_experiment.py
→ Outputs: data/extended_experiment_all_runs.csv

4.generate figures:
python plot_results.py
→ Outputs: figures/*.png

All results are deterministic and reproducible with the provided seed.

🖼️ Sample Figures

Participation by Spillover	Trust × Spillover Heatmap
Left: Participation rate collapses completely under any spillover.
Right: Vertical boundary confirms initial trust cannot offset spillover risk.

📘 Model Specification (ODD Protocol)
Purpose: Simulate how negative spillovers undermine cooperation in a pension governance system.
Entities:
Citizens: Update trust via Bayesian learning + social influence; decide to participate.
Brokers: Generate returns; may suffer scandals (negative shocks).
Process: Each step: (i) brokers realize outcomes, (ii) spillover updates global trust, (iii) citizens revise trust, (iv) citizens decide to contribute.
Design Concepts: Emergence, Interaction, Stochasticity, Adaptation.
Details: See model.py and paper appendix.
📚 Citation
If you use this model, please cite:
@article{xu2026trust,
  title={Trust Collapse Under Negative Spillover: An Agent-Based Model of Collaborative Governance with Implications for China's Personal Pension System},
  author={Xu, J.},
  journal={Journal of Artificial Societies and Social Simulation},
  year={2026}
}
Code available at: https://github.com/yourusername/trust_abm


📄 License
MIT License. See LICENSE for details.
🔗 Data DOI
[![DOI](https://zenodo.org/badge/1155171850.svg)](https://doi.org/10.5281/zenodo.18605927)







