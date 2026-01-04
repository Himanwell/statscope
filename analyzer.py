"""
Data analysis functions
Handles all data processing and insight generation
"""

import pandas as pd
import textwrap
import matplotlib.pyplot as plt
import seaborn as sns

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO


# Dataset overview


def identify_date_range(df):
    for col in df.columns:
        if df[col].dtype == "object":
            dates = pd.to_datetime(df[col], errors="coerce")
            if dates.notna().mean() > 0.7:
                return f"{dates.min().date()} to {dates.max().date()}"
    return "No date column detected"

def get_dataset_overview(df):
    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "date_range": identify_date_range(df),
    }


# Data quality


def check_missing_data(df):
    missing = df.isnull().sum()
    return [
        {
            "column": col,
            "count": int(missing[col]),
            "percentage": (missing[col] / len(df)) * 100
        }
        for col in missing[missing > 0].index
    ]


# Numeric insight


def generate_numeric_insight(column, series, beginner=True):
    mean, min_val, max_val = series.mean(), series.min(), series.max()

    if beginner:
        return (
            f"This column shows {column}. "
            f"Most values are around {mean:.1f}. "
            f"Values usually fall between {min_val:.1f} and {max_val:.1f}."
        )

    return f"For {column}, the mean is {mean:.2f}."

def is_likely_identifier(series, column_name, df):
    name = column_name.lower()
    if "id" in name or "uuid" in name:
        return True
    return series.nunique() / len(df) > 0.95

def analyze_numeric_columns(df, max_columns=3, beginner=True):
    results = []
    for col in df.select_dtypes(include="number").columns:
        series = df[col].dropna()
        if series.empty or is_likely_identifier(series, col, df):
            continue

        results.append({
            "column": col,
            "mean": series.mean(),
            "median": series.median(),
            "min": series.min(),
            "max": series.max(),
            "std": series.std(),
            "outlier_count": 0,
            "insight": generate_numeric_insight(col, series, beginner),
            "values": series.values
        })

        if len(results) >= max_columns:
            break

    return results


# Correlations


def find_correlations(df, threshold=0.5):
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        return []
    corr = numeric.corr()

    results = []
    for i in range(len(corr.columns)):
        for j in range(i + 1, len(corr.columns)):
            if abs(corr.iloc[i, j]) >= threshold:
                results.append({
                    "column1": corr.columns[i],
                    "column2": corr.columns[j],
                    "correlation": corr.iloc[i, j],
                    "direction": "positive" if corr.iloc[i, j] > 0 else "negative"
                })
    return results

def get_correlation_matrix(df):
    numeric = df.select_dtypes(include="number")
    return numeric.corr() if numeric.shape[1] >= 2 else None


# Categorical


def analyze_categorical_columns(df, max_columns=2):
    results = []
    for col in df.select_dtypes(include="object").columns[:max_columns]:
        results.append({
            "column": col,
            "unique_count": df[col].nunique(),
            "top_values": df[col].value_counts().head(10)
        })
    return results

# --------------------------------------------------
# PDF REPORT
# --------------------------------------------------

def generate_pdf_report(dataset_name, overview, numeric, corr_matrix, categories):

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin_x, y = 50, height - 50

    def new_page():
        nonlocal y
        c.showPage()
        y = height - 50
        c.setFont("Helvetica", 11)

    # TITLE
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin_x, y, "Statscope Report")
    y -= 25

    c.setFont("Helvetica-Oblique", 11)
    c.drawString(margin_x, y, f"Dataset: {dataset_name}")
    y -= 30

    # OVERVIEW
    c.setFont("Helvetica", 11)
    c.drawString(margin_x, y, f"Rows: {overview['total_rows']}")
    y -= 15
    c.drawString(margin_x, y, f"Columns: {overview['total_columns']}")
    y -= 15
    c.drawString(margin_x, y, f"Date range: {overview['date_range']}")
    y -= 30

    # NUMERIC
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin_x, y, "Numeric Insights")
    y -= 20

    for stat in numeric:
        if y < 250:
            new_page()

        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin_x, y, stat["column"])
        y -= 15

        for line in textwrap.wrap(stat["insight"], 90):
            c.setFont("Helvetica", 11)
            c.drawString(margin_x, y, line)
            y -= 14

        fig, ax = plt.subplots(figsize=(4, 2))
        ax.hist(stat["values"], bins=20, color="skyblue")
        ax.set_title(stat["column"])
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=150)
        plt.close(fig)
        buf.seek(0)

        c.drawImage(ImageReader(buf), margin_x, y - 120, 300, 120)
        y -= 150

    # CORRELATION HEATMAP
    if corr_matrix is not None:
        new_page()
        c.setFont("Helvetica-Bold", 13)
        c.drawString(margin_x, y, "Correlation Heatmap")
        y -= 20

        fig, ax = plt.subplots(figsize=(4, 4))
        sns.heatmap(corr_matrix, cmap="coolwarm", ax=ax)
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=150)
        plt.close(fig)
        buf.seek(0)

        c.drawImage(ImageReader(buf), margin_x, y - 300, 300, 300)

    c.save()
    buffer.seek(0)
    return buffer
