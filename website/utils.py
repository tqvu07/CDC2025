import pandas as pd

# Load your CSV
df = pd.read_csv("planets.csv")  # replace with your CSV filename

# Filter habitable zone
hz = df[(df["Insolation Flux [Earth Flux]"] >= 0.35) &
        (df["Insolation Flux [Earth Flux]"] <= 1.7)]

# Only Earth-size-ish planets
hz = hz[hz["Planet radius (earth radius)"] <= 2]

# Sort by distance from Earth
hz = hz.sort_values(by="Distance [pc]")

# Save JSON for the website
hz.to_json("hz_planets.json", orient="records")
print("JSON file generated!")