#!/usr/bin/env python3
"""Download and chart UK service corridors with India and China."""
from __future__ import annotations

import io
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"
for folder in (DATA, TABLES, FIGURES):
    folder.mkdir(parents=True, exist_ok=True)

BASE = "https://sdmx.oecd.org/public/rest/v1/data/OECD.SDD.TPS,DSD_BATIS@DF_BATIS,1.0/"
PAIRS = [
    ("GBR", "IND", "UK imports from India"),
    ("IND", "GBR", "India imports from UK"),
    ("GBR", "CHN", "UK imports from China"),
    ("CHN", "GBR", "China imports from UK"),
]
SERVICES = {
    "SJ3": "Technical and other business services (SJ3)",
    "SE": "Construction services (SE)",
    "SI": "Computer and information services (SI)",
}


def download() -> pd.DataFrame:
    frames = []
    for importer, exporter, label in PAIRS:
        for service, service_name in SERVICES.items():
            key = f"{importer}.{exporter}.M.S.{service}.A.USD_EXC.B"
            url = BASE + key
            response = requests.get(
                url,
                params={"startPeriod": "2015", "endPeriod": "2024"},
                headers={"Accept": "text/csv"},
                timeout=60,
            )
            response.raise_for_status()
            frame = pd.read_csv(io.StringIO(response.text))
            if frame.empty:
                raise RuntimeError(f"No BaTIS observations returned for {key}")
            frame["corridor"] = label
            frame["service_name"] = service_name
            frame["source_url"] = response.url
            frames.append(frame)
    data = pd.concat(frames, ignore_index=True)
    keep = [
        "REF_AREA",
        "COUNTERPART_AREA",
        "TRADE_FLOW",
        "SERVICE",
        "TIME_PERIOD",
        "OBS_VALUE",
        "ADJUSTMENT",
        "UNIT_MEASURE",
        "OBS_STATUS",
        "corridor",
        "service_name",
        "source_url",
    ]
    data = data[keep].sort_values(["corridor", "SERVICE", "TIME_PERIOD"])
    data.to_csv(DATA / "batis_uk_india_china.csv", index=False)
    return data


def summary_table(data: pd.DataFrame) -> pd.DataFrame:
    wide = data.pivot_table(
        index=["corridor", "SERVICE", "service_name"],
        columns="TIME_PERIOD",
        values="OBS_VALUE",
        aggfunc="first",
    ).reset_index()
    table = wide[["corridor", "SERVICE", "service_name", 2019, 2024]].copy()
    table = table.rename(columns={2019: "usd_mn_2019", 2024: "usd_mn_2024"})
    table["change_pct_2019_2024"] = (
        (table["usd_mn_2024"] / table["usd_mn_2019"] - 1) * 100
    )
    for col in ["usd_mn_2019", "usd_mn_2024", "change_pct_2019_2024"]:
        table[col] = table[col].round(1)
    table.to_csv(TABLES / "table_uk_india_china_corridors.csv", index=False)
    return table


def plot_sj3(data: pd.DataFrame) -> None:
    frame = data[data.SERVICE == "SJ3"].copy()
    base = frame[frame.TIME_PERIOD == 2019].set_index("corridor").OBS_VALUE
    frame["index_2019_100"] = frame.apply(
        lambda row: row.OBS_VALUE / base[row.corridor] * 100, axis=1
    )
    fig, ax = plt.subplots(figsize=(9.2, 5.5))
    for corridor, group in frame.groupby("corridor", sort=False):
        ax.plot(
            group.TIME_PERIOD,
            group.index_2019_100,
            marker="o",
            linewidth=2,
            label=corridor,
        )
    ax.axhline(100, color="#777777", linewidth=0.8, linestyle="--")
    ax.set(
        title="The United Kingdom’s SJ3 service corridors with India and China",
        xlabel="Year",
        ylabel="Index (2019 = 100)",
    )
    ax.legend(frameon=False, ncol=2)
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURES / "figure22_uk_india_china_sj3.png", dpi=220)
    plt.close(fig)


def plot_growth(table: pd.DataFrame) -> None:
    service_order = ["SJ3", "SE", "SI"]
    corridor_order = [label for _, _, label in PAIRS]
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.8), sharey=True)
    colors = ["#2864a6", "#d67a1f", "#3b8b5a", "#8b5fa8"]
    for ax, service in zip(axes, service_order):
        part = table[table.SERVICE == service].set_index("corridor")
        values = [part.loc[c, "change_pct_2019_2024"] for c in corridor_order]
        bars = ax.barh(corridor_order, values, color=colors)
        ax.set_title(service)
        ax.axvline(0, color="#333333", linewidth=0.8)
        ax.grid(axis="x", alpha=0.2)
        for bar, value in zip(bars, values):
            ax.text(value + 2, bar.get_y() + bar.get_height() / 2, f"{value:.0f}%", va="center")
    axes[0].set_ylabel("Bilateral import flow")
    fig.suptitle("Growth in UK–India and UK–China services trade, 2019–2024")
    fig.supxlabel("Change in balanced import value (%)")
    fig.tight_layout()
    fig.savefig(FIGURES / "figure23_uk_india_china_service_growth.png", dpi=220)
    plt.close(fig)


def main() -> None:
    data = download()
    table = summary_table(data)
    plot_sj3(data)
    plot_growth(table)
    print("observations", len(data))
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
