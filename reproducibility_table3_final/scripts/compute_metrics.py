import yaml
import pandas as pd

with open("configs/experiment.yaml") as f:
    cfg = yaml.safe_load(f)

df = pd.read_csv(cfg["output"]["raw_results"])

summary = df.groupby("nodes").agg(
    accuracy_mean=("accuracy", "mean"),
    accuracy_std=("accuracy", "std"),
    precision_mean=("precision", "mean"),
    precision_std=("precision", "std"),
    recall_mean=("recall", "mean"),
    recall_std=("recall", "std"),
    f1_mean=("f1", "mean"),
    f1_std=("f1", "std"),
    epochs_mean=("epochs", "mean"),
    epochs_std=("epochs", "std"),
    time_mean=("time_sec", "mean"),
    time_std=("time_sec", "std")
)

summary.to_csv(cfg["output"]["summary"])
print("Metric summary generated")
