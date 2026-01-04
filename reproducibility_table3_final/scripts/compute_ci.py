import yaml
import pandas as pd
import numpy as np

with open("configs/experiment.yaml") as f:
    cfg = yaml.safe_load(f)

df = pd.read_csv(cfg["output"]["summary"])

N = cfg["num_runs"]
Z = cfg["statistics"]["z_value"]

for col in df.columns:
    if col.endswith("_std"):
        df[col.replace("_std", "_ci")] = Z * (df[col] / np.sqrt(N))

df.to_csv(cfg["output"]["summary_ci"], index=False)
print("95% confidence intervals computed")
