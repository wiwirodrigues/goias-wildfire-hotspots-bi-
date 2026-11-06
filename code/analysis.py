"""
Heat-hotspot recurrence in Goias state parks, 2016-2025.
Reproduces every statistic reported in the README and the executive presentation.

Input : data/focos_e_parques_31982.gpkg (original QGIS export, one row per hotspot)
Output: printed report and code/results.csv
Needs : numpy, pandas, scipy
Run   : python code/analysis.py
"""
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "focos_e_parques_31982.gpkg"
CELL_DEG = 0.01          # grid size: 0.01 degree is about 1.1 km
SAME_FIRE_DAYS = 180     # hotspots closer than this in the same cell are one fire
END = pd.Timestamp("2025-12-31 23:59:59")   # end of the observation window
DAYS_PER_YEAR = 365.25
SEED = 42
results = []


def report(name, value):
    """Print a result and keep it for results.csv."""
    results.append({"statistic": name, "value": value})
    print(f"{name:<58} {value}")


# ---------------------------------------------------------------- 1. load data
def load():
    # A .gpkg file is a SQLite database, so no GIS library is required.
    with sqlite3.connect(SOURCE) as con:
        df = pd.read_sql(
            """SELECT DataHora, DiaSemChuv, Precipitac, RiscoFogo, FRP,
                      nome_uc AS park, lat_pbi AS lat, lon_pbi AS lon
               FROM focos_e_parques_31982""", con)
    df["time"] = pd.to_datetime(df["DataHora"])
    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month
    # INPE codes a missing fire risk as -999.
    df["RiscoFogo"] = df["RiscoFogo"].where(df["RiscoFogo"] != -999)
    return df


# ------------------------------------------------- 2. from hotspots to fire events
def add_cells(df, size=CELL_DEG):
    """Assign each hotspot to the nearest point of a regular grid."""
    out = df.copy()
    out["cy"] = np.round(out["lat"] / size).astype(int)
    out["cx"] = np.round(out["lon"] / size).astype(int)
    return out


def build_events(df):
    """One row per fire event. A new event starts when a cell has been quiet
    for at least 180 days. Detections in the overlap of two parks are counted
    once here, because recurrence is measured by cell, not by park."""
    d = df.drop_duplicates(["DataHora", "lat", "lon"]).sort_values("time").copy()
    gap = d.groupby(["cy", "cx"])["time"].diff().dt.total_seconds() / 86400
    d["new_event"] = gap.isna() | (gap >= SAME_FIRE_DAYS)
    d["event_id"] = d.groupby(["cy", "cx"])["new_event"].cumsum()
    ev = (d.groupby(["cy", "cx", "event_id"])
            .agg(start=("time", "min"), frp=("FRP", "mean"), park=("park", "first"),
                 n=("time", "size"))
            .reset_index().sort_values(["cy", "cx", "start"]))
    # Intervals use whole days between the first hotspot of each event.
    ev["interval"] = ev.groupby(["cy", "cx"])["start"].diff().dt.days / DAYS_PER_YEAR
    return ev


# ------------------------------------------------------------------ 3. statistics
def kaplan_meier(time, event, at):
    """Share re-burned by each time in `at`, with a Greenwood 95% CI.
    Cells that never burned again are censored at the end of the window."""
    order = np.argsort(time)
    time, event = np.asarray(time)[order], np.asarray(event)[order]
    surv, var_sum, curve = 1.0, 0.0, []
    for t in np.unique(time[event == 1]):
        at_risk = (time >= t).sum()
        deaths = ((time == t) & (event == 1)).sum()
        surv *= 1 - deaths / at_risk
        if at_risk > deaths:
            var_sum += deaths / (at_risk * (at_risk - deaths))
        curve.append((t, surv, surv * np.sqrt(var_sum)))
    out = {}
    for a in at:
        past = [c for c in curve if c[0] <= a]
        s, se = (past[-1][1], past[-1][2]) if past else (1.0, 0.0)
        out[a] = (1 - s, 1 - s - 1.96 * se, 1 - s + 1.96 * se)
    return out


def logit_cluster(X, y, groups):
    """Logistic regression by Newton-Raphson with cluster-robust errors.
    Clustering by cell corrects for repeated years of the same cell."""
    b = np.zeros(X.shape[1])
    for _ in range(50):
        p = 1 / (1 + np.exp(-X @ b))
        H = (X * (p * (1 - p))[:, None]).T @ X
        step = np.linalg.solve(H, X.T @ (y - p))
        b += step
        if np.abs(step).max() < 1e-10:
            break
    p = 1 / (1 + np.exp(-X @ b))
    bread = np.linalg.inv((X * (p * (1 - p))[:, None]).T @ X)
    scores = pd.DataFrame(X * (y - p)[:, None]).groupby(groups).sum().values
    G = len(scores)
    n, k = X.shape
    adj = G / (G - 1) * (n - 1) / (n - k)
    vcov = adj * bread @ (scores.T @ scores) @ bread
    return b, np.sqrt(np.diag(vcov))


def cell_years(cells):
    """Panel of one row per cell and year, from the year after the first
    hotspot to 2025. A cell counts as burned in a year if it had any hotspot
    that year. `since` is the number of calendar years since the last burn."""
    d = cells.drop_duplicates(["DataHora", "lat", "lon"])
    rows = []
    for (cy, cx), g in d.groupby(["cy", "cx"]):
        fire_years = sorted(set(g["year"]))
        last = fire_years[0]
        for year in range(last + 1, 2026):
            burned = year in fire_years
            rows.append((f"{cy}_{cx}", year, year - last, int(burned)))
            if burned:
                last = year
    return pd.DataFrame(rows, columns=["cell", "year", "since", "burned"])


def mann_kendall(x):
    """Mann-Kendall trend test with tie correction, plus Sen's slope."""
    x = np.asarray(x, float)
    n = len(x)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    s = sum(np.sign(x[j] - x[i]) for i, j in pairs)
    _, ties = np.unique(x, return_counts=True)
    var = (n * (n - 1) * (2 * n + 5) - (ties * (ties - 1) * (2 * ties + 5)).sum()) / 18
    z = (s - np.sign(s)) / np.sqrt(var) if s else 0.0
    p = 2 * stats.norm.sf(abs(z))
    tau = s / (n * (n - 1) / 2)
    slope = np.median([(x[j] - x[i]) / (j - i) for i, j in pairs])
    return slope, p, tau


def morans_i(values, xy, k=8, perms=999):
    """Moran's I with k-nearest-neighbour weights and a permutation p-value."""
    rng = np.random.default_rng(SEED)
    dist = np.linalg.norm(xy[:, None, :] - xy[None, :, :], axis=2)
    np.fill_diagonal(dist, np.inf)
    nb = np.argsort(dist, axis=1)[:, :k]

    def moran(v):
        z = v - v.mean()
        return len(v) / nb.size * (z * z[nb].sum(axis=1)).sum() / (z ** 2).sum()

    observed = moran(values)
    sims = np.array([moran(rng.permutation(values)) for _ in range(perms)])
    return observed, ((sims >= observed).sum() + 1) / (perms + 1)


def main():
    df = load()
    report("Hotspots (rows)", len(df))
    report("Unique detections", len(df.drop_duplicates(["DataHora", "lat", "lon"])))
    report("Hotspots with FRP", int(df["FRP"].notna().sum()))
    report("Missing fire risk", int(df["RiscoFogo"].isna().sum()))

    # Concentration in space and time
    by_park = df["park"].value_counts()
    print(by_park.to_string())
    report("Share in top 2 parks %", round(by_park.iloc[:2].sum() / len(df) * 100, 1))
    by_month = df["month"].value_counts().reindex(range(1, 13), fill_value=0)
    print(by_month.to_string())
    report("Share Aug-Oct %", round(by_month.loc[8:10].sum() / len(df) * 100, 1))
    peak = df.groupby(["year", "month"]).size().unstack(fill_value=0).idxmax(axis=1)
    report("Years with September peak", int((peak == 9).sum()))

    # Recurrence
    cells = add_cells(df)
    report("Burned cells (cell)", cells[["cy", "cx"]].drop_duplicates().shape[0])
    report("Burned cells (park + cell)",
           cells[["park", "cy", "cx"]].drop_duplicates().shape[0])
    ev = build_events(cells)
    iv = ev["interval"].dropna()
    per_cell = ev.groupby(["cy", "cx"]).size()
    report("Fire events", len(ev))
    report("Recurrences", len(iv))
    report("Cells burned more than once", int((per_cell > 1).sum()))
    report("Median interval", round(iv.median(), 2))
    report("Mean interval", round(iv.mean(), 2))
    whole = iv.round().astype(int).value_counts().sort_index()
    print(pd.DataFrame({"n": whole, "%": (whole / len(iv) * 100).round(1),
                        "cum%": (whole.cumsum() / len(iv) * 100).round(1)}).to_string())

    # Is the median interval 3 years? Is the share below 3 years above 50%?
    w = stats.wilcoxon(iv - 3, method="approx", correction=False)
    r = abs(stats.norm.isf(w.pvalue / 2)) / np.sqrt(len(iv))
    report("Wilcoxon p / r", f"{w.pvalue:.3f} / {r:.2f}")
    below = int((iv < 3).sum())
    b = stats.binomtest(below, len(iv), 0.5, alternative="greater")
    h = 2 * np.arcsin(np.sqrt(below / len(iv))) - 2 * np.arcsin(np.sqrt(.5))
    report("Binomial below 3y / p / h", f"{below} / {b.pvalue:.3f} / {h:.2f}")

    # Time from the first fire to the next one, per cell
    g = ev.groupby(["cy", "cx"])["start"]
    first, nxt = g.transform("min"), g.shift(-1)
    base = ev[ev["start"] == first].assign(nxt=nxt[ev["start"] == first])
    t = np.where(base["nxt"].notna(), (base["nxt"] - base["start"]).dt.days,
                 (END - base["start"]).dt.days) / DAYS_PER_YEAR
    km = kaplan_meier(t, base["nxt"].notna().astype(int).values, [1, 2, 3])
    for a, (v, lo, hi) in km.items():
        report(f"KM re-burned within {a}y % (first fire)",
               f"{v*100:.1f} ({lo*100:.1f}-{hi*100:.1f})")

    # Annual chance of a new fire
    panel = cell_years(cells)
    report("Cell-years", len(panel))
    table = panel[panel["since"] <= 4].groupby("since")["burned"].agg(["mean", "size"])
    print(table.round(3).to_string())
    X = np.c_[np.ones(len(panel)), (panel["since"] == 1).astype(int)]
    y = panel["burned"].values.astype(float)
    beta, se = logit_cluster(X, y, panel["cell"].values)
    z = beta[1] / se[1]
    report("Logit OR (year 1 vs later) [95% CI] p",
           f"{np.exp(beta[1]):.2f} [{np.exp(beta[1]-1.96*se[1]):.2f}-"
           f"{np.exp(beta[1]+1.96*se[1]):.2f}] p={2*stats.norm.sf(abs(z)):.4f}")
    report("Risk year 1 vs later %",
           f"{y[panel['since']==1].mean()*100:.1f} vs {y[panel['since']>1].mean()*100:.1f}")

    # Weather and hotspots
    m = df.groupby("month").agg(n=("time", "size"), rain_free=("DiaSemChuv", "mean"),
                                prec=("Precipitac", "mean"), risk=("RiscoFogo", "mean"))
    ym = df.groupby(["year", "month"]).agg(n=("time", "size"), rain_free=("DiaSemChuv", "mean"))
    for lab, a, b_ in [("rain-free days x hotspots, monthly", m["rain_free"], m["n"]),
                       ("fire risk x hotspots, monthly", m["risk"], m["n"]),
                       ("precipitation x hotspots, monthly", m["prec"], m["n"]),
                       ("rain-free days x hotspots, year-month", ym["rain_free"], ym["n"])]:
        s = stats.spearmanr(a, b_)
        pr = stats.pearsonr(a, b_)
        report(f"Spearman {lab} (n={len(a)})",
               f"rho={s.statistic:.2f} p={s.pvalue:.3f} | Pearson r={pr.statistic:.2f} p={pr.pvalue:.3f}")

    # Fire intensity: short vs long intervals
    rec = ev[ev["interval"].notna() & ev["frp"].notna()]
    short, long_ = rec.loc[rec["interval"] < 3, "frp"], rec.loc[rec["interval"] >= 3, "frp"]
    mw = stats.mannwhitneyu(short, long_)
    report("Mann-Whitney FRP median <3 vs >=3 / p",
           f"{short.median():.2f} vs {long_.median():.2f} / {mw.pvalue:.3f} (n={len(rec)})")

    # Differences between parks
    rp = ev[ev["interval"].notna()]
    groups = [v["interval"].values for _, v in rp.groupby("park")]
    H = stats.kruskal(*groups)
    k, n = len(groups), len(rp)
    report("Kruskal-Wallis interval H(df) p e2",
           f"H({k-1})={H.statistic:.1f} p={H.pvalue:.4g} e2={(H.statistic-k+1)/(n-k):.3f}")
    print(rp.groupby("park")["interval"].median().round(1).to_string())
    fd = df[df["FRP"].notna()]
    groups = [v["FRP"].values for _, v in fd.groupby("park") if len(v) > 1]
    H = stats.kruskal(*groups)
    k, n = len(groups), sum(map(len, groups))
    report("Kruskal-Wallis FRP H(df) p e2",
           f"H({k-1})={H.statistic:.1f} p={H.pvalue:.4g} e2={(H.statistic-k+1)/(n-k):.3f}")

    # Seasonality and trend
    chi = stats.chisquare(by_month.values)
    report("Chi-square months / Cramer V",
           f"{chi.statistic:.0f} / {np.sqrt(chi.statistic/(len(df)*11)):.2f}")
    yearly = df["year"].value_counts().sort_index()
    report("Mann-Kendall hotspots slope p tau",
           "{:.1f} {:.3f} {:.2f}".format(*mann_kendall(yearly.values)))
    ev_year = ev["start"].dt.year.value_counts().reindex(range(2016, 2026), fill_value=0)
    report("Mann-Kendall events slope p tau",
           "{:.1f} {:.3f} {:.2f}".format(*mann_kendall(ev_year.values)))

    # Spatial clustering of hotspots per burned cell
    cnt = cells.groupby(["cy", "cx"]).size().reset_index(name="n")
    i, p = morans_i(cnt["n"].values.astype(float), cnt[["cx", "cy"]].values.astype(float))
    report("Moran's I (8 neighbours, burned cells) / p", f"{i:.2f} / {p:.3f}")

    # Normality of each variable
    for lab, s in [("interval", iv), ("FRP", df["FRP"].dropna()),
                   ("rain-free days", df["DiaSemChuv"]), ("precipitation", df["Precipitac"]),
                   ("fire risk", df["RiscoFogo"].dropna())]:
        sw = stats.shapiro(s)
        report(f"Normality {lab} (n={len(s)})",
               f"mean={s.mean():.2f} median={s.median():.2f} skew={stats.skew(s):.2f} SW p={sw.pvalue:.2g}")

    # Sensitivity to cell size
    for size in [0.0034, 0.01, 0.02, 0.05]:  # ~375 m, ~1.1 km, ~2.2 km, ~5 km
        c2 = add_cells(df, size)
        e2 = build_events(c2)
        g2 = e2.groupby(["cy", "cx"])["start"]
        f2 = g2.transform("min")
        b2 = e2[e2["start"] == f2].assign(nxt=g2.shift(-1)[e2["start"] == f2])
        t2 = np.where(b2["nxt"].notna(), (b2["nxt"] - b2["start"]).dt.days,
                      (END - b2["start"]).dt.days) / DAYS_PER_YEAR
        k3 = kaplan_meier(t2, b2["nxt"].notna().astype(int).values, [3])[3][0]
        p2 = cell_years(c2)
        y1, y2 = [p2.loc[p2["since"] == s, "burned"].mean() * 100 for s in (1, 2)]
        report(f"Cell {size}: cells / 3y re-burn % / median / y1->y2",
               f"{len(b2)} / {k3*100:.1f} / {e2['interval'].median():.1f} / {y1:.1f}->{y2:.1f}")

    pd.DataFrame(results).to_csv(ROOT / "code" / "results.csv", index=False)


if __name__ == "__main__":
    main()
