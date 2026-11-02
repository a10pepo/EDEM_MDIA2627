<!-- ======================= HEADER ======================= -->
<div align="center">

<img src="./assets/banner.svg" alt="Carlos Candela Giner - Mathematician, AI and Data Scientist" width="100%"/>

<a href="https://github.com/CarlosCandela02">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=18&pause=1200&color=38BDF8&center=true&vCenter=true&width=820&height=50&lines=Bridging+mathematical+first+principles+and+business+value;Statistical+Modeling+%7C+Machine+Learning+%7C+LLM+Engineering;From+Bayesian+inference+to+production-grade+AI;Turning+uncertainty+into+decisions" alt="Typing SVG" />
</a>

<br/><br/>

<a href="https://www.linkedin.com/in/carlos-candela-giner-70126430a/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="mailto:candelaginercarlos@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
<img src="https://img.shields.io/badge/Based_in-Valencia,_Spain-1e293b?style=for-the-badge&logo=googlemaps&logoColor=38bdf8" alt="Location"/>
<img src="https://img.shields.io/badge/Open_to-Europe-10b981?style=for-the-badge&logo=europeanunion&logoColor=white" alt="Open to Europe"/>

</div>

<br/>

---

## `01.` // The Core Philosophy

> I build AI systems grounded in strict mathematical theory — **convergence, probabilistic modeling and uncertainty propagation** — to solve real business and engineering problems.

$$
\hat{x}_{k|k} = \hat{x}_{k|k-1} + K_k\left(z_k - H_k\,\hat{x}_{k|k-1}\right), \qquad
K_k = P_{k|k-1}H_k^\top\left(H_k P_{k|k-1}H_k^\top + R_k\right)^{-1}
$$

*The Kalman filter update: optimal decisions require continuously revising our beliefs as new data arrives.*

<table>
<tr>
<td width="55%" valign="top">

```python
class CarlosCandela(DataScientist):
    education = {
        "BSc":  "Mathematics · Universitat de València",
        "BSc ": "Biomedical Engineering",
        "MSc":  "Business Management",
        "MSc ": "AI, Big Data & Cloud · EDEM",
    }
    core = {
        "stochastic": ["Dynamic Linear Models",
                       "Kalman Filtering",
                       "Bayesian Inference"],
        "ml":         ["LLM Engineering",
                       "Random Forests",
                       "Deep Learning"],
        "biostats":   ["Survival Analysis",
                       "Cox PH", "Kaplan-Meier"],
    }

    def deliver_value(self, data, goal):
        model = self.design(data, rigor="strict")
        return model.deploy(target=goal)
```

</td>
<td width="45%" valign="top">

**What drives me**

- 📐 Rigor first: understand *why* a model works before shipping it
- 🔬 Honest uncertainty: intervals, not just point estimates
- 🚀 Models that leave the notebook and create value
- 🌍 Looking for my next challenge in **Europe**

</td>
</tr>
</table>

---

## `02.` // Experience & Applied Research

<table>
<tr>
<td width="60"><h2>🧠</h2></td>
<td>

**AI & Data Engineer — Matil**
Built automated pipelines with **Python, advanced Regex and LLM prompt engineering** to extract and structure complex data from energy and gas invoices.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![LLMs](https://img.shields.io/badge/LLM_Engineering-412991?style=flat-square) ![Regex](https://img.shields.io/badge/Regex-0f172a?style=flat-square) ![ETL](https://img.shields.io/badge/Data_Pipelines-38bdf8?style=flat-square)

</td>
</tr>
<tr>
<td><h2>🌫️</h2></td>
<td>

**Spatiotemporal Modeling — BSc Mathematics Final Project**
Analyzed and forecasted **PM<sub>2.5</sub>** pollution in Valencia with **Dynamic Linear Models**, Kalman filtering and Fourier seasonal components.

![DLM](https://img.shields.io/badge/Dynamic_Linear_Models-1e3a8a?style=flat-square) ![Kalman](https://img.shields.io/badge/Kalman_Filter-1e3a8a?style=flat-square) ![R](https://img.shields.io/badge/R-276DC3?style=flat-square&logo=r&logoColor=white)

</td>
</tr>
<tr>
<td><h2>🧬</h2></td>
<td>

**Clinical Survival Analysis**
Developed mortality prediction models for clinical cohorts, combining **Cox Proportional Hazards, Kaplan-Meier curves and Random Forests**.

![Survival](https://img.shields.io/badge/Survival_Analysis-10b981?style=flat-square) ![RF](https://img.shields.io/badge/Random_Forest-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)

</td>
</tr>
</table>

---

## `03.` // Technical Arsenal

<div align="center">

<img src="https://skillicons.dev/icons?i=py,r,matlab,postgres,pytorch,sklearn,git,docker,vscode,gcp,bash&perline=11" alt="Skills"/>

<br/>

<img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy"/>
<img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas"/>
<img src="https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white" alt="SciPy"/>

</div>

| Domain | Stack |
| :-- | :-- |
| **Languages** | Python · R · MATLAB · SQL |
| **ML & Statistics** | PyTorch · Scikit-Learn · SciPy · Bayesian inference · State-space models · Survival analysis |
| **LLMs** | Prompt engineering · Structured extraction · Evaluation |
| **Cloud & Tools** | GCP · Docker · Git · VS Code · RStudio |

---

## `04.` // Work Paradigm

```mermaid
graph LR
    A[Raw / Unstructured Data] --> B(Preprocessing · Regex · NLP)
    B --> C{Analytical Core}
    C -->|Time Series| D[Dynamic Models · Kalman Filters]
    C -->|Machine Learning| E[Ensembles · Deep Learning · LLMs]
    C -->|Clinical / Risk| F[Survival Analysis · Bayesian Stats]
    D --> G[Business Impact & Production]
    E --> G
    F --> G
    style A fill:#0f172a,stroke:#64748b,color:#fff
    style B fill:#0f172a,stroke:#64748b,color:#fff
    style C fill:#1e3a8a,stroke:#38bdf8,stroke-width:3px,color:#fff
    style D fill:#0f172a,stroke:#38bdf8,color:#fff
    style E fill:#0f172a,stroke:#38bdf8,color:#fff
    style F fill:#0f172a,stroke:#38bdf8,color:#fff
    style G fill:#064e3b,stroke:#10b981,stroke-width:3px,color:#fff
```

---

## `05.` // Featured Projects

<!-- Replace the links with your real repositories -->

| Project | What it does | Stack |
| :-- | :-- | :-- |
| 🌫️ [**PM2.5 DLM Forecasting**](https://github.com/CarlosCandela02/REPO_PM25) | Probabilistic forecasting of air quality in Valencia with state-space models | `R` `DLM` `Kalman` |
| 🧾 [**Invoice Extraction with LLMs**](https://github.com/CarlosCandela02/REPO_FACTURAS) | Structured extraction from energy invoices | `Python` `LLM` `Regex` |
| 🧬 [**Clinical Survival Models**](https://github.com/CarlosCandela02/REPO_SURVIVAL) | Cox PH vs. Random Survival Forests on clinical cohorts | `Python` `R` `Survival` |

---

## `06.` // GitHub Stats

<div align="center">

<a href="https://github.com/CarlosCandela02?tab=repositories"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Fusers%2FCarlosCandela02&query=%24.public_repos&label=Public%20repos&color=1e3a8a&style=for-the-badge&logo=github" alt="Public repos"/></a>
<a href="https://github.com/CarlosCandela02?tab=followers"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Fusers%2FCarlosCandela02&query=%24.followers&label=Followers&color=0f172a&style=for-the-badge&logo=github" alt="Followers"/></a>
<img src="https://streak-stats.demolab.com?user=CarlosCandela02&theme=tokyonight&hide_border=true&background=0d1117" alt="Streak"/>

</div>

---

## `07.` // Let's Connect

<div align="center">

I'm interested in roles in **data science, ML engineering and applied AI** across Europe.

<a href="https://www.linkedin.com/in/carlos-candela-giner-70126430a/"><img src="https://img.shields.io/badge/Let's_talk-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="mailto:candelaginercarlos@gmail.com"><img src="https://img.shields.io/badge/Write_me-Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>

<img src="./assets/footer.svg" alt="Footer" width="100%"/>

</div>