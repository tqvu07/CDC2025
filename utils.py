import pandas as pd
import numpy as np

# -------------------------
# Load CSV
# -------------------------
csv_file = "planets.csv"  # replace with your CSV filename
df = pd.read_csv(csv_file, comment='#')  # skip comment lines if present

# -------------------------
# Required columns
# -------------------------
required_cols = [
    "pl_name", "hostname", "pl_rade", "sy_dist", "pl_orbsmax",
    "st_rad", "st_teff"
]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

df = df.dropna(subset=required_cols)

# -------------------------
# Calculate stellar luminosity
# L_star = (R_star / R_sun)^2 * (T_star / T_sun)^4
# -------------------------
T_sun = 5778  # K
df['L_star'] = (df['st_rad']**2) * (df['st_teff']/T_sun)**4

# -------------------------
# Habitable zone boundaries (AU)
# Conservative estimates from Kopparapu et al. 2013
# -------------------------
HZ_inner = 0.95 * np.sqrt(df['L_star'])
HZ_outer = 1.37 * np.sqrt(df['L_star'])

# -------------------------
# Filter planets in habitable zone
# -------------------------
hz = df[(df['pl_orbsmax'] >= HZ_inner) & (df['pl_orbsmax'] <= HZ_outer)]

# Only Earth-size-ish planets
hz = hz[hz["pl_rade"] <= 2]

# Sort by distance from Earth
hz = hz.sort_values(by="sy_dist")

# -------------------------
# Rename columns for website
# -------------------------
hz = hz.rename(columns={
    "pl_name": "Planet Name",
    "hostname": "Host name",
    "sy_dist": "Distance [pc]",
    "pl_rade": "Planet radius (earth radius)",
    "pl_orbsmax": "Semi-major Axis (AU)"
})

# -------------------------
# Save JSON
# -------------------------
hz.to_json("hz_planets.json", orient="records")
print(f"Saved {len(hz)} habitable planets to hz_planets.json")