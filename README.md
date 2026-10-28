# Does a 3-Year Fire Rule Hold in the Cerrado? Heat-Hotspot Recurrence in Goiás State Parks


> **Support for Wildfire Prevention Planning in Goiás State Parks Based on Hotspots**

![Power BI](https://img.shields.io/badge/Power%20BI-Interactive%20Dashboard-yellow?style=for-the-badge&logo=powerbi)
![Cerrado](https://img.shields.io/badge/Biome-Cerrado-green?style=for-the-badge)
![CBMGO](https://img.shields.io/badge/Domain-Wildfire%20Management-red?style=for-the-badge)

# Does a 3-Year Fire Rule Hold in the Cerrado? Heat-Hotspot Recurrence in Goiás State Parks - Brazil

Power BI, QGIS and Excel analysis of 2,774 satellite heat hotspots recorded in 9 Goiás state parks between 2016 and 2025. The Goiás Military Fire Department (CBMGO) received a study stating that, after a fire, fuel takes about **three years** to recover before the same area can burn again. If that held in Goiás, recently burned areas could be left out of inspection rounds for three years. This project tests whether the study's interval applies to the Cerrado, explains why it does not, and proposes a safer way to prioritize prevention.

**[View the interactive Power BI dashboard](https://app.powerbi.com/view?r=eyJrIjoiNWRkNDQwN2QtOGRjOS00NjMwLTkzNTctMTBkMDZmZjY2YzhlIiwidCI6Ijk1NDYxM2ZhLWUzN2UtNDZkNi04NGYxLTJmYjNmMzY3MjExMyJ9)**
##  Sample Delimitation

Of the 12 Conservation Units (State Parks) originally mapped in the State of Goiás, the spatio-temporal analysis focused on **9 State Parks** that presented valid records of heat focus recurrence:

* Águas do Paraíso State Park
* Águas Lindas State Park
* Altamiro de Moura Pacheco State Park
* Araguaia State Park
* João Leite State Park
* Paraúna State Park
* Pirineus State Park
* Serra Dourada State Park
* Terra Ronca State Park

> **Methodological Note:** The *Mata Atlântica*, *Serra de Caldas Novas*, and *Serra de Jaraguá* state parks were not included in the final sample due to the absence of temporal recurrence records within the analyzed period. This absence stems from inherent limitations of satellite remote sensing — such as sensor orbit timing not coinciding with the active fire event, short-duration fires that cease thermal anomaly emissions prior to the satellite overpass, or cloud cover interference during scanning.


## Key Findings

- **The 3-year interval does not hold in Goiás state parks.** Among 501 recurrent hotspots, the most common interval is **2 years** (mode), and **41.5%** came back within 2 years (208 of 501), inside the window the study would have left unchecked.
- **The average agreed with the study, but the distribution did not.** The mean interval is **3.05 years**, close to the study's 3 years. The distribution is spread out, though, with about one quarter each at 2, 3 and 4 years, so 3 years is an average, not a safe minimum.
- **Why so fast? Grasses are the leading explanation.** Cerrado studies report that the native grass layer recovers 70–80% of its biomass one year after fire and about 100% after two years, and invasive African grasses add even more fuel. This matches the 2-year mode. The external study was run outside the Cerrado and did not address grasses.
- **What to do instead: focus on where and when.** Terra Ronca and Serra Dourada hold **71.3%** of all hotspots, and hotspots concentrate between **August and October**. Days without rain show a moderate positive correlation with hotspots (r = 0.41).
- **Recommendation:** do not adopt the 3-year skip. Keep recently burned areas on the inspection list and prioritize park sectors by hotspot history, season and drought, back-testing the ranking after each fire season.

## Project Overview

This project, originally a capstone (TCC) at CBMGO, was restructured with a problem-solving method (**DEASA**: Define, Structure, Analyze, Solutions, Present):

1. **Define** the problem with the ACERT framework (explained below).
2. **Structure** it as a hypothesis tree with necessary conditions, plus a MECE root-cause tree.
3. **Analyze** the data with QGIS and Excel, check the ecological conditions against the literature, and build a Power BI dashboard.
4. **Develop solutions** prioritized by evidence, impact and feasibility.
5. **Present** the results in an executive deck built on the pyramid principle.

## Business Problem

**Central question:** does the study's 3-year fuel-recovery interval hold for Goiás state parks, so that CBMGO can safely leave recently burned areas out of inspection rounds?

**What is ACERT?** ACERT is a problem-definition checklist created by mentor Ale Saito (EdukaNegócios) and taught as the first step of the DEASA method. It is not a widely known framework, so here is what each letter stands for. **ACERT is a Portuguese acronym**, which is why the letters do not match the English terms (for example, A = *Atores interessados* = Stakeholders, and E = *Escopo* = Scope):


| Letter | Portuguese | English | Question it answers |
| --- | --- | --- | --- |
| **A** | Atores interessados | Stakeholders | Who decides, who is affected and who will use the result? |
| **C** | Critérios de sucesso | Success criteria | How will we know the problem has been solved? |
| **E** | Escopo | Scope | What is included in the analysis, and what is left out? |
| **R** | Restrições | Restrictions | Which limits on data, resources or rules must the analysis respect? |
| **T** | Tempo | Time | What is the deadline, and which period do the data cover? |

Applied to this project:

<img width="1452" height="792" alt="acert_firehp" src="https://github.com/user-attachments/assets/24dd203f-09a0-4d80-99ea-d36a826d7e2e" />

## Hypothesis Tree

The question arrived as a closed hypothesis ("the 3-year interval applies here"), so it was structured as a **hypothesis tree with necessary conditions (AND logic)**: every condition must be true for the hypothesis to hold, and one false condition is enough to reject it. The three branches use different kinds of evidence (the project data, the ecology of the Cerrado and the validity of the measurement), which keeps them mutually exclusive.

<img width="1443" height="806" alt="image" src="https://github.com/user-attachments/assets/738d9150-0ea0-4f6f-82de-f2fef400200a" />

C1 was tested first, because it can be answered directly with the hotspot data and decides the operational question. C2 was checked against the Cerrado literature, since no vegetation data was available.

A hypothesis tree carries a known risk of confirmation bias. Here it was used the other way around: to stress-test a belief the stakeholders already held.

### Root-cause tree: why does the Cerrado burn again so fast?

Once the hypothesis was rejected, a second, exploratory tree mapped the possible causes in four MECE branches: fuel, weather, ignition and site. Each leaf is tagged with the kind of evidence available.

![Root-cause tree](assets/why_tree.png)

## Dataset

**Heat hotspots** from INPE's [BDQueimadas](https://terrabrasilis.dpi.inpe.br/queimadas/bdqueimadas/) and **state park boundaries** from SIGA, the Goiás State Environmental Geoinformation System. After the spatial overlay, the analysis included **2,774 hotspots** and **501 recurrent hotspots**.

| Variable | Description |
| --- | --- |
| Park | State park where the hotspot falls (after the QGIS overlay) |
| DateTime | Date and time of the satellite detection |
| Latitude, Longitude | Hotspot coordinates |
| DaysWithoutRain | Consecutive days without rain at detection |
| Precipitation | Precipitation (mm) |
| FireRisk | INPE fire-risk index |
| FRP | Fire Radiative Power (MW) |
| IRFC_years | Interval of Recurrence of Heat Hotspots: years between consecutive hotspots at the same approximate location |

A **commander survey** (Google Forms, 11 closed Likert questions) was answered by 16 CBMGO unit commanders (94.1% response rate; 87.5% Majors or Captains, 81% with 11 to 30 years of service).

## Data Preparation (QGIS and Excel)

- Downloaded hotspots for 2016–2025 and the park polygons
- Overlaid hotspots on the park boundaries in QGIS, keeping only hotspots inside the 9 parks (2,774)
- Approximated locations by truncating coordinates, so hotspots close to each other count as the same location
- Identified locations with hotspots in more than one year (501 recurrent hotspots) and calculated the **IRFC** in years
- Split João Leite and Altamiro de Moura Pacheco into 4 management sectors to test concentration inside parks
- Loaded the data into Power BI with a calendar dimension (year, month) and a park dimension

## Analysis Approach

### Why these methods

- **Frequency distribution with mode and cumulative %** for recurrence. The study proposes a cut-off ("3 years"), so the useful question is *what share of re-burns happen before it* and *what the most common interval is*, not only what the average is.
- **Literature review** for the ecological condition (C2), since the project has no vegetation data.
- **Share of total (Pareto view)** for spatial concentration, a distribution question that needs no test.
- **Pearson correlation** for weather, since both hotspot counts and weather variables are quantitative.

### What these methods do *not* tell us, and how this was handled

| Limitation | How it was handled |
| --- | --- |
| The mean can hide operational risk | Mode, median and cumulative shares reported alongside the mean |
| A heat hotspot is not a confirmed fire or a mapped burned area | Results are read as *hotspot recurrence* (C3 marked as partial); validation with MapBiomas Fire burned-area maps listed as a next step |
| Coordinate truncation groups nearby hotspots | A recurrence means "hotspots again at the same approximate location", not the same patch of vegetation |
| Literature evidence is not local evidence | Grasses are presented as the leading explanation, not as a tested result |
| Larger parks naturally collect more hotspots | Counts reported as shares; normalization by area (hotspots per 100 km²) listed as a next step |
| Pearson measures linear association only and does not prove causation | Weather treated as an alert signal, not a cause |

## Results

<img width="1455" height="806" alt="image" src="https://github.com/user-attachments/assets/33f0a288-2053-48fc-8450-5c882733b1f7" />


| Condition | Main finding | Verdict |
| --- | --- | --- |
| C1.1 Few recurrences within 2 years | 41.5% within ≤ 2 years (208 of 501); 63.9% within ≤ 3 years | **Rejected** |
| C1.2 The most frequent interval is 3+ years | Mode = 2 years (25.9%); mean 3.05; median 3 | **Rejected** |
| C1.3 The pattern holds in every park | IRFC not yet calculated by park | Not tested (next step) |
| C2.1 The study's vegetation is similar to the Cerrado | The study was run outside the Cerrado and did not address grasses | **Rejected** |
| C2.2 Cerrado grass fuel needs about 3 years to recover | Native grass layer: 70–80% of biomass after 1 year, about 100% after 2 years | **Rejected** (literature) |
| C3.1 A recurrent hotspot means the same area burned again | Approximate location (truncated coordinates) | Partial |
| C3.2 Each hotspot is a real, detected fire | Hotspots are an indirect indicator | Partial |

**Verdict:** the hypothesis is rejected. Two necessary conditions fail, one with local data (C1) and one with the literature (C2). C3 limits how precisely re-burns are measured, but not the direction of the conclusion.

![Recurrence](assets/02_recurrence.png)

| IRFC | Count | % | Cumulative % |
| --- | --- | --- | --- |
| 1 year | 78 | 15.6% | 15.6% |
| 2 years | 130 | 25.9% | 41.5% |
| 3 years | 112 | 22.4% | 63.9% |
| 4 years | 117 | 23.4% | 87.2% |
| 5 years | 23 | 4.6% | 91.8% |
| 6 years | 15 | 3.0% | 94.8% |
| 7 years | 25 | 5.0% | 99.8% |
| 8 years | 1 | 0.2% | 100% |
| **Total** | **501** | **100%** | |

### Why so fast: the grass hypothesis

The data show *that* the Cerrado re-burns faster than the study suggested. The literature suggests *why*:

- **The native grass layer recovers quickly.** In Cerrado *campo sujo*, about 70–80% of ground-layer biomass returns one year after fire, and about 100% after two years (Andrade, 1998; Neto et al., 1998, cited in Gorgone-Barbosa et al., 2016; Onigemo, Miranda & Haridasan, 2003).
- **Invasive African grasses add fuel.** Species such as *Melinis minutiflora* (capim-gordura) and *Urochloa* spp. (braquiária) accumulate more biomass than native species, and flames in invaded plots were up to twice as tall (Gorgone-Barbosa et al., 2016; Pivello et al., 2021).
- **This matches the 2-year mode in the data**, while the 3-year interval came from a different ecosystem.

![Why so fast](assets/03_why_so_fast.png)

This explanation is supported by the literature but **was not tested with project data**, because no vegetation data was available. Testing it is the first next step.

### What to do instead: where and when

| Analysis | Main finding |
| --- | --- |
| Hotspots by park | Terra Ronca 50.7% + Serra Dourada 20.6% = **71.3%** of all hotspots |
| Hotspots by sector | 2 of 4 sectors = **89%** of 333 hotspots (João Leite + Altamiro) |
| Seasonality | August to October, peaking in September in every year |
| Days without rain | r = 0.41 (positive, moderate) |
| Precipitation | r = −0.30 (negative, weak) |
| Commander survey | 93.8% agree the dashboard supports planning; 100% would use it; 93% report lack of personnel |

![Spatial concentration](assets/04_spatial_concentration.png)

![Timing and adoption](assets/05_timing_and_adoption.png)

## Power BI Dashboard

- **KPI card:** total heat hotspots (2,774)
- **Hotspots by month and year:** seasonal curve for each year, 2016–2025
- **Ranking of parks** by total hotspots
- **Hotspot map** with each point colored by year
- **Heat map** of hotspot density across the state
- **Filters:** year, month and park

[![Dashboard preview](assets/dashboard_preview.png)](https://app.powerbi.com/view?r=eyJrIjoiNWRkNDQwN2QtOGRjOS00NjMwLTkzNTctMTBkMDZmZjY2YzhlIiwidCI6Ijk1NDYxM2ZhLWUzN2UtNDZkNi04NGYxLTJmYjNmMzY3MjExMyJ9)

**[Open the interactive dashboard](https://app.powerbi.com/view?r=eyJrIjoiNWRkNDQwN2QtOGRjOS00NjMwLTkzNTctMTBkMDZmZjY2YzhlIiwidCI6Ijk1NDYxM2ZhLWUzN2UtNDZkNi04NGYxLTJmYjNmMzY3MjExMyJ9)** (no login required)

| Hotspot map | Heat map |
| --- | --- |
| ![Hotspot map](assets/dashboard_map.png) | ![Heat map](assets/dashboard_heatmap.png) |

## Recommendations and Action Plan

| Initiative | Priority | Proposed decision |
| --- | --- | --- |
| Do not adopt the 3-year skip; keep recently burned areas in inspection rounds | 1 | Decide before the next fire season |
| Risk-based ranking of park sectors (history, month, drought) | 2 | Pilot for one fire season and back-test |
| Concentrate preventive resources on Terra Ronca and Serra Dourada before August | 3 | Plan firebreaks and patrols in June–July |
| Test the grass hypothesis with MapBiomas land-cover and burned-area maps | 4 | Compare re-burn intervals by vegetation type |
| Split every park into management sectors and normalize by park area | Investigate | Improve the dashboard before scaling the ranking |


**Pilot (5W2H):** before the season, rank park sectors by hotspot history, month and days without rain; keep recently burned sectors in the rounds; build firebreaks and patrol schedules in June–July; after the August–October season, compare the ranking with where new hotspots fell. Success indicators: **hit rate** (share of new hotspots in top-priority sectors) and **miss rate** (share in deprioritized sectors).

Rough sizing: had the 3-year skip been applied, **208 of the 501 recurrences (41.5%)** would have happened in areas off the inspection list, and up to 320 (63.9%) if year 3 were also skipped.

<img width="1435" height="792" alt="image" src="https://github.com/user-attachments/assets/4ab1e8d3-867f-4998-a3a5-4c36788478b5" />


## Limitations

- Heat hotspots are an indirect indicator: one fire can generate many hotspots, and small fires may go undetected.
- Recurrence is measured in whole years at an approximate location (truncated coordinates).
- No local data on vegetation, grass cover or biomass: the grass explanation relies on the literature.
- No data on ignition causes or human activity around the parks.
- Hotspot counts are not normalized by park area; correlations show association, not causation.
- The survey covers 16 commanders and was applied while the dashboard was still under development.

**Next steps:** calculate IRFC by park (C1.3); use MapBiomas Fire burned-area and land-cover maps to compare re-burn intervals in grassland, savanna and invaded areas; normalize by park area.

## Tools

- **QGIS:** spatial overlay of hotspots and park boundaries
- **Excel:** cleaning, coordinate approximation, IRFC calculation, frequency tables and Pearson correlation
- **Power BI:** interactive dashboard
- **Google Forms:** commander survey
- **PowerPoint:** problem structuring (ACERT, hypothesis trees, action plan) and executive presentation
- **GitHub:** documentation and version control

## Project Structure

```
goias-wildfire-hotspots-bi/
│
├── README.md
│
├── data/
│   ├── README.md              (data dictionary)
│   └── heat_hotspots_2016_2025.csv
│
├── powerbi/
│   └── wildfire_hotspots_dashboard.pbix
│
├── presentation/
│   └── wildfire_executive_presentation_EN.pptx
│
└── assets/
    ├── 01–06 presentation slides (.png)
    ├── method_acert.png
    ├── hypothesis_tree.png, hypothesis_results.png, why_tree.png
    ├── action_plan.png
    └── dashboard_preview.png, dashboard_map.png, dashboard_heatmap.png
```

## References

- *[External study on the 3-year fuel-recovery interval: citation to be added]*
- Gorgone-Barbosa, E.; Pivello, V. R.; Rissi, M. N.; Zupo, T.; Fidelis, A. (2016). A importância da consideração de espécies invasoras no manejo integrado do fogo. *Biodiversidade Brasileira*, 6(2), 27–40.
- Onigemo, A. E.; Miranda, H. S.; Haridasan, M. (2003). Efeitos de queimadas bienais e quadrienais sucessivas sobre a biomassa do estrato rasteiro de campo sujo de cerrado. *Anais do VI Congresso de Ecologia do Brasil*, 360–362.
- Pivello, V. R. et al. (2021). Understanding Brazil's catastrophic fires: causes, consequences and policy needed to prevent future tragedies. *Perspectives in Ecology and Conservation*, 19(3), 233–255.
- MapBiomas (2025). *RAF 2024: Annual Fire Report, Collection 4 (1985–2024).*
