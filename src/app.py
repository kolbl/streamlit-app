"""Streamlit dashboard: groundhog forecasts from groundhog-day.com API."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.request import urlopen

import pandas as pd
import streamlit as st

from data_analytics.column_statistics import (
    calculate_max_of_column,
    calculate_min_of_column,
)

# Workshop: comment out the next line to hide active duration, and comment
# it back in once calculate_span_of_column is part of the package.
# from data_analytics.column_statistics import calculate_span_of_column

API_URL = "https://groundhog-day.com/api/v1/groundhogs"

GROUNDHOG_KEYS = [
    "groundhog_id",
    "slug",
    "name",
    "city",
    "region",
    "country",
    "type",
]


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_groundhogs() -> list[dict]:
    """Download and parse the public groundhogs JSON."""
    with urlopen(API_URL, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("groundhogs", [])


def predictions_to_dataframe(groundhogs: list[dict]) -> pd.DataFrame:
    """Flatten nested predictions into one row per (groundhog, year)."""
    rows: list[dict] = []
    for gh in groundhogs:
        meta = {
            "groundhog_id": gh.get("id"),
            "slug": gh.get("slug"),
            "name": gh.get("name"),
            "shortname": gh.get("shortname"),
            "city": gh.get("city"),
            "region": gh.get("region"),
            "country": gh.get("country"),
            "type": gh.get("type"),
            "active": gh.get("active"),
            "description": (gh.get("description") or "").strip(),
            "image_url": (gh.get("image") or "").strip(),
            "source_url": (gh.get("source") or "").strip(),
            "current_prediction_url": (
                gh.get("currentPrediction") or ""
            ).strip(),
        }
        for pred in gh.get("predictions") or []:
            row = {**meta}
            row["year"] = pred.get("year")
            row["shadow"] = pred.get("shadow")
            row["details"] = pred.get("details")
            rows.append(row)
    return pd.DataFrame(rows)


def year_span(years: pd.DataFrame):
    """Years between first and last prediction.

    Returns None when the calculate_span_of_column import above is commented out.
    """
    try:
        span = calculate_span_of_column(years, "year")
    except NameError:
        return None
    if pd.isna(span):
        return None
    return span


def groundhog_summary_stats(pred_df: pd.DataFrame) -> pd.DataFrame:
    """Per-groundhog year span (min/max) and shadow rate among known outcomes."""
    rows: list[dict] = []
    for key, group in pred_df.groupby(GROUNDHOG_KEYS, dropna=False):
        sub_y = group[["year"]].copy()
        sub_y["year"] = pd.to_numeric(sub_y["year"], errors="coerce")
        meta = dict(
            zip(
                GROUNDHOG_KEYS,
                key if isinstance(key, tuple) else (key,),
            )
        )
        meta["prediction_start_year"] = calculate_min_of_column(sub_y, "year")
        meta["prediction_end_year"] = calculate_max_of_column(sub_y, "year")
        meta["prediction_year_span"] = year_span(sub_y)
        shadow_known = group["shadow"].dropna()
        meta["p_saw_shadow_if_known"] = (
            float(shadow_known.astype("float64").mean())
            if len(shadow_known)
            else float("nan")
        )
        rows.append(meta)
    return pd.DataFrame(rows)


def groundhog_catalog_table(
    pred_df: pd.DataFrame, shadow_rows: pd.DataFrame
) -> pd.DataFrame:
    """One row per groundhog with static fields, span, and shadow rate."""
    meta = pred_df.drop_duplicates(subset=["groundhog_id"], keep="first")
    keep = [
        "groundhog_id",
        "slug",
        "name",
        "shortname",
        "city",
        "region",
        "country",
        "type",
        "description",
        "image_url",
        "source_url",
        "current_prediction_url",
    ]
    keep = [c for c in keep if c in meta.columns]
    meta = meta[keep]
    stats = shadow_rows[
        [
            "groundhog_id",
            "prediction_start_year",
            "prediction_end_year",
            "prediction_year_span",
            "p_saw_shadow_if_known",
        ]
    ].drop_duplicates(subset=["groundhog_id"])
    return meta.merge(stats, on="groundhog_id", how="left")


def main() -> None:
    st.set_page_config(
        page_title="Groundhog forecasts",
        page_icon="🦫",
        layout="wide",
    )
    st.title("Groundhog Day forecast statistics")
    st.caption(
        "Data from [groundhog-day.com](https://groundhog-day.com) "
        f"([API]({API_URL})). "
        "“Shadow” ≈ longer winter; no shadow ≈ early spring. "
        "Null means no recorded outcome for that year."
    )
    st.markdown(
        """Groundhog Day is a lighthearted holiday celebrated annually across North America
in which ‘prognosticating’ animals predict the onset of spring.

Traditionally, on February 2nd, various groundhogs across North America are
consulted by local public figures (often a mayor) for an annual weather
prediction:

- If the groundhog ‘sees its shadow’, it means 6 more weeks of winter
- If the groundhog doesn’t see its shadow, spring will come early
"""
    )

    try:
        groundhogs = fetch_groundhogs()
    except URLError as e:
        st.error(f"Could not reach the API: {e}")
        st.stop()
    except (json.JSONDecodeError, OSError) as e:
        st.error(f"Failed to read response: {e}")
        st.stop()

    if not groundhogs:
        st.warning("No groundhogs returned.")
        st.stop()

    pred_df = predictions_to_dataframe(groundhogs)
    shadow_rows = groundhog_summary_stats(pred_df)

    catalog_df = groundhog_catalog_table(pred_df, shadow_rows)

    st.subheader("Groundhogs")
    notes = [
        "Prediction **timespan** uses ``calculate_min_of_column`` / "
        "``calculate_max_of_column`` on ``year``."
    ]
    if "calculate_span_of_column" in globals():
        notes.append(
            "**Active duration** uses ``calculate_span_of_column`` "
            "(last year minus first year)."
        )
    notes.append(
        "Shadow share is the mean of ``shadow`` over years with a recorded value."
    )
    st.caption(" ".join(notes))
    for _, row in catalog_df.sort_values("name").iterrows():
        ys, ye = row["prediction_start_year"], row["prediction_end_year"]
        if pd.notna(ys) and pd.notna(ye):
            span = f"{int(ys)}–{int(ye)}"
        else:
            span = "—"
        span_years = row.get("prediction_year_span")
        title = f"{row['name']} · {span}"
        with st.expander(title, expanded=False):
            c1, c2 = st.columns([1, 2])
            with c1:
                img = str(row.get("image_url") or "").strip()
                if img:
                    try:
                        st.image(img, width=220)
                    except Exception:
                        st.caption("Image could not be loaded.")
                else:
                    st.caption("No image.")
            with c2:
                loc = f"{row.get('city', '')}, {row.get('region', '')}"
                st.markdown(f"**{loc}** · {row.get('country', '')}")
                st.caption(f"_{row.get('type', '')}_")
                desc = str(row.get("description") or "").strip()
                if desc:
                    st.markdown(desc)
                else:
                    st.caption("No description.")
                src = str(row.get("source_url") or "").strip()
                cur = str(row.get("current_prediction_url") or "").strip()
                if src:
                    st.markdown(f"[Source / history]({src})")
                if cur:
                    st.markdown(f"[Current prediction]({cur})")
                rate = row.get("p_saw_shadow_if_known")
                if pd.notna(rate):
                    st.caption(
                        f"Share of recorded years with shadow: **{rate:.1%}**"
                    )
                if pd.notna(span_years):
                    st.caption(f"Active for **{int(span_years)}** years.")


if __name__ == "__main__":
    main()
