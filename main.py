import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

roll_number = 102303077

a_r = 0.05 * (roll_number % 7)
b_r = 0.3 * ((roll_number % 5) + 1)

print("a_r:", a_r)
print("b_r:", b_r)

file_path = "data/air_quality.csv"
df = pd.read_csv(file_path, encoding="latin1")

df.columns = df.columns.str.strip()

no2_column = None
for col in df.columns:
    if "NO2" in col.upper():
        no2_column = col
        break

if no2_column is None:
    raise ValueError("NO2 column not found")

no2_values = pd.to_numeric(df[no2_column], errors="coerce").dropna()

x = no2_values.values

z = x + a_r * np.sin(b_r * x)

mu = np.mean(z)
variance = np.var(z)
lam = 1 / (2 * variance)
c = 1 / np.sqrt(2 * np.pi * variance)

print("\nEstimated Parameters:")
print("mu =", mu)
print("lambda =", lam)
print("c =", c)

plt.figure(figsize=(8,5))
plt.hist(z, bins=50, density=True, alpha=0.6)

z_range = np.linspace(min(z), max(z), 1000)
pdf = c * np.exp(-lam * (z_range - mu)**2)

plt.plot(z_range, pdf)
plt.title("Gaussian Fit on Transformed NO2")
plt.xlabel("z")
plt.ylabel("Density")

plt.savefig("images/gaussian_fit.png")
plt.show()
