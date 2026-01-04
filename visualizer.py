"""
Visualization functions
Creates all charts and graphs
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_distribution_chart(data, column_name):
    bins = min(50, int(np.sqrt(len(data))))

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.hist(data, bins=bins, color="skyblue", edgecolor="black")
    ax.set_title(f"Distribution of {column_name}")
    ax.set_xlabel(column_name)
    ax.set_ylabel("Count")

    # Auto-adjust layout
    plt.tight_layout()
    return fig


def create_correlation_heatmap(corr_matrix):
    fig, ax = plt.subplots(figsize=(8, 6))

    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        center=0,
        ax=ax
    )

    ax.set_title("How the numbers relate to each other")

    # Human-friendly explanation BELOW the chart
    explanation = (
        "How to read this:\n"
        "• Values close to 1 mean strong positive relationship\n"
        "• Values close to -1 mean strong negative relationship\n"
        "• Values near 0 mean little or no relationship\n"
        "• Darker colors = stronger relationship\n\n"
        "Reminder: Correlation shows association, not cause-and-effect."
    )

    # Place text at the figure level (not axes)
    fig.text(
        0.5,           # centered horizontally
        -0.25,         # pushed below the plot
        explanation,
        ha="center",
        va="top",
        fontsize=10,
        wrap=True
    )

    # Reserve space at the bottom for explanation
    plt.tight_layout(rect=[0, 0.15, 1, 1])

    return fig


def create_category_bar_chart(value_counts, column_name):
    fig, ax = plt.subplots(figsize=(8, 4))
    value_counts.plot(kind="bar", ax=ax, color="lightcoral")

    ax.set_title(f"Most common values in {column_name}")
    ax.set_xlabel(column_name)
    ax.set_ylabel("Count")
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    return fig
