import pandas as pd

# -----------------------------
# 1️⃣ Load CSV safely
# -----------------------------
try:
    # comment='#' skips all lines starting with '#'
    df = pd.read_csv("planets.csv", comment='#', on_bad_lines='skip')
    print(f"CSV loaded successfully: {len(df)} rows")
except FileNotFoundError:
    print("Error: planets.csv not found in the current folder")
    exit()
except pd.errors.ParserError as e:
    print("ParserError:", e)
    exit()

# -----------------------------
# 2️⃣ Clean column names
# -----------------------------
df.columns = df.columns.str.strip().str.lower()  # remove spaces + lowercase

# -----------------------------
# 3️⃣ Remove repeated header rows (if any)
# -----------------------------
if 'pl_name' in df.columns:
    df = df[df['pl_name'] != 'pl_name']  # remove repeated header rows
else:
    print("Error: 'pl_name' column not found!")
    exit()

# -----------------------------
# 4️⃣ Check required columns exist
# -----------------------------
required_columns = ['pl_name', 'hostname', 'sy_dist', 'pl_rade', 'pl_insol']
missing = [col for col in required_columns if col not in df.columns]
if missing:
    print(f"Error: Missing required columns: {missing}")
    exit()

# -----------------------------
# 5️⃣ Filter habitable zone planets
# -----------------------------
hz = df[(df["pl_insol"].notna()) & (df["pl_insol"] >= 0.35) & (df["pl_insol"] <= 1.7)]
hz = hz[(hz["pl_rade"].notna()) & (hz["pl_rade"] <= 2)]

# -----------------------------
# 6️⃣ Sort by distance
# -----------------------------
hz = hz.sort_values(by="sy_dist")

# -----------------------------
# 7️⃣ Keep only necessary columns and rename
# -----------------------------
hz = hz[["pl_name", "hostname", "sy_dist", "pl_rade", "pl_insol"]]
hz = hz.rename(columns={
    "pl_name": "Planet Name",
    "hostname": "Host name",
    "sy_dist": "Distance [pc]",
    "pl_rade": "Planet radius (earth radius)",
    "pl_insol": "Insolation Flux [Earth Flux]"
})

# -----------------------------
# 8️⃣ Export JSON
# -----------------------------
hz.to_json("hz_planets.json", orient="records", indent=2)
print(f"JSON generated with {len(hz)} habitable planets: hz_planets.json")