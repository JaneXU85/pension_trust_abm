# Trust Dynamics in Collaborative Governance: An ABM Study

This repository contains the source code and data for the paper:

> **"Trust Collapse Under Negative Spillover: An Agent-Based Model of Collaborative Governance with Implications for China's Personal Pension System"**

Submitted to *Journal of Artificial Societies and Social Simulation (JASSS)*.

## 📌 Overview
We investigate how negative spillover effects—where localized trust breaches propagate across a network—undermine cooperation in a broker-mediated governance system inspired by China’s personal pension framework. Using agent-based modeling (ABM), we show that negative spillover drives final trust to zero regardless of initial trust levels (p < 0.001).

## 📂 Repository Structure
├── agents.py # Stakeholder agent definition
├── model.py # Main model logic (CollaborativeGovernanceModel)
├── run_experiments.py # Full factorial experiment (180 runs)
├── stat_test.py # Statistical analysis and visualization
├── experiment_all_runs.csv # Raw results from 180 simulation runs
├── boxplot_trust.png # Final trust distribution by condition
├── trust_analysis.png # Initial vs. final trust scatter plot
└── requirements.txt # Python dependencies


## ▶️ How to Reproduce

### Prerequisites
- Python 3.8+
- Conda (recommended)

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/trust_abm.git
   cd trust_abm

2.Create and activate conda environment:
conda env create -f environment.yml
conda activate abm_trust

3.Run the full experiment (takes ~2 minutes):
python run_experiments.py

4.Perform statistical analysis and generate figures:
python stat_test.py

You should see:
experiment_all_runs.csv generated
boxplot_trust.png and trust_analysis.png saved
📊 Key Results
Without negative spillover: Mean final trust = 0.133
With negative spillover: Mean final trust = 0.000
Statistical significance: p < 0.001 for both groups (t-test, n=90 per group)
📚 Citation
If you use this work, please cite our paper (once published) and acknowledge the code:
Author. (2025). Trust Collapse Under Negative Spillover... Journal of Artificial Societies and Social Simulation.
Code available at: https://github.com/yourusername/trust_abm

📄 License
MIT License. See LICENSE for details.
🔗 Data DOI
![DOI](https://zenodo.org/badge/XXXXXX.svg)
(Will be updated after Zenodo deposit)

5. **保存**（Ctrl + S），关闭。

---

### 🔧 文件 2：创建 `requirements.txt`

1. 右键 → 新建 → 文本文档
2. 改名为：`requirements.txt`
3. 右键编辑，粘贴：

```txt
mesa==2.2.4
pandas>=1.5.0
numpy>=1.21.0
scipy>=1.9.0
seaborn>=0.12.0
matplotlib>=3.6.0
