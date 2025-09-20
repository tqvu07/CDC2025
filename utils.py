import pandas as pd

# -------------------------
# Load CSV
# -------------------------
csv_file = "planets.csv"  # replace with your CSV filename
df = pd.read_csv(csv_file, comment='#')  # skip comment lines if present

# -------------------------
# Keep only required columns and drop rows with missing values
# -------------------------
required_cols = ["pl_name", "hostname", "pl_rade", "sy_dist", "pl_insol"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

df = df.dropna(subset=required_cols)

# -------------------------
# Filter habitable zone
# -------------------------
hz = df[(df["pl_insol"] >= 0.35) & (df["pl_insol"] <= 1.7)]

# Only Earth-size-ish planets
hz = hz[hz["pl_rade"] <= 2]

# -------------------------
# Sort by distance from Earth
# -------------------------
hz = hz.sort_values(by="sy_dist")

# -------------------------
# Rename columns to match your JSON/HTML keys
# -------------------------
hz = hz.rename(columns={
    "pl_name": "Planet Name",
    "hostname": "Host name",
    "sy_dist": "Distance [pc]",
    "pl_rade": "Planet radius (earth radius)",
    "pl_insol": "Insolation Flux [Earth Flux]"
})

# -------------------------
# Save JSON for website
# -------------------------
output_file = "hz_planets.json"
hz.to_json(output_file, orient="records")
print(f"Saved {len(hz)} habitable planets to {output_file}")