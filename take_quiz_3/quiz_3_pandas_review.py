# Quiz 3 Practice Notebook — Subsetting, Grouping, Replacing, Merging
# ============================================================
# Covers Lectures 11, 14, 15, and 16
# ============================================================

import pandas as pd
import numpy as np

# ----------------------------------
# 1. Load Dataset (example: circuits)
# ----------------------------------

circuits = pd.read_csv("circuits.csv")
print(circuits.head())

# ============================================================
# Lecture 11 – Subsetting Data
# ============================================================

# Example: Subset using logical condition
subset_example = circuits.query("lat > 0 and country == 'USA'")
print(subset_example.head())

# ============================================================
# Lecture 14 – Renaming & Replacing
# ============================================================

# Rename one column (leaving others unchanged)
circuits = circuits.rename(columns={"name": "circuit_name"})
print(circuits.columns)

# Replace specific values in one line using .replace()
circuits["country"] = circuits["country"].replace({
    "USA": "United States",
    "UK": "United Kingdom",
    "UAE": "United Arab Emirates"
})
print(circuits["country"].unique())

# ============================================================
# Lecture 15 – Grouping & Aggregating
# ============================================================

# Example dataset (simulate results)
df_results = pd.DataFrame({
    "raceId": [1, 1, 2, 2, 3, 3],
    "constructorId": [10, 20, 10, 20, 10, 20],
    "points": [10, 8, 6, 9, 12, 5]
})

# Group and aggregate multiple statistics
df_grouped = (
    df_results.groupby("constructorId")
    .agg(
        mean_points=("points", "mean"),
        max_points=("points", "max"),
        min_points=("points", "min"),
        sd_points=("points", "std")
    )
)
print(df_grouped)

# Subset, group, and aggregate in one line
subset_group_agg = (
    df_results.query("raceId >= 2")
    .groupby(["raceId", "constructorId"])
    .agg(mean_points=("points", "mean"), max_points=("points", "max"))
)
print(subset_group_agg)

# ============================================================
# Lecture 16 – Sorting and Merging
# ============================================================

# Sort by aggregated value in descending order
df_constructor_points_agg = (
    df_results.groupby("constructorId")["points"]
    .agg(avgpoints=("mean"))
    .sort_values(by="avgpoints", ascending=False)
)
print(df_constructor_points_agg)

# Example merge operation
df_races_new = pd.DataFrame({
    "raceId": [1, 2, 3],
    "year": [2020, 2021, 2022],
    "circuitId": [101, 102, 103]
})

df_circuits_new = circuits.rename(columns={"circuitId": "circuitId", "circuit_name": "circuit_name"})

merged = pd.merge(
    left=df_races_new,
    right=df_circuits_new[["circuitId", "circuit_name", "location"]],
    on="circuitId",
    how="left"
)
print(merged.head())

# ============================================================
# Practice Exercises (Quiz 3 Style)
# ============================================================

# 1️⃣ Replace values
test_replace = circuits.copy()
test_replace["country"] = test_replace["country"].replace({"United States": "USA"})
print(test_replace.head())

# 2️⃣ Subset + Group + Aggregate
test_subset_group = (
    df_results.query("points >= 8")
    .groupby("constructorId")
    .agg(mean_points=("points", "mean"))
)
print(test_subset_group)

# 3️⃣ Recode numeric variable into categorical variable
circuits["lat_category"] = np.where(
    circuits["lat"] < 0,
    "Southern Hemisphere",
    "Northern Hemisphere"
)
print(circuits[["circuit_name", "lat", "lat_category"]].head())

# 4️⃣ Group + Sort
df_sorted = (
    df_results.groupby("constructorId")["points"]
    .agg(avgpoints=("mean"))
    .sort_values(by="avgpoints", ascending=False)
)
print(df_sorted)

# 5️⃣ Rename column example
circuits_renamed = circuits.rename(columns={"location": "city"})
print(circuits_renamed.columns)

# 6️⃣ Merge example
merged_example = pd.merge(df_races_new, circuits[["circuitId", "circuit_name", "country"]], on="circuitId", how="left")
print(merged_example.head())
