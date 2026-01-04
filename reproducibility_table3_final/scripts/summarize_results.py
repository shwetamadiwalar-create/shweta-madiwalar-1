import yaml
import pandas as pd

with open("configs/experiment.yaml") as f:
    cfg = yaml.safe_load(f)

df = pd.read_csv(cfg["output"]["summary_ci"])

print("\n===== TABLE 3: Scalability Performance (Mean ± 95% CI) =====\n")
print("Nodes | Accuracy | Precision | Recall | F1-score | Epochs | Time(s)")
print("-" * 78)

for _, r in df.iterrows():
    print(
        f"{int(r['nodes'])} | "
        f"{r['accuracy_mean']:.1f}±{r['accuracy_ci']:.1f} | "
        f"{r['precision_mean']:.1f}±{r['precision_ci']:.1f} | "
        f"{r['recall_mean']:.1f}±{r['recall_ci']:.1f} | "
        f"{r['f1_mean']:.1f}±{r['f1_ci']:.1f} | "
        f"{int(r['epochs_mean'])}±{int(r['epochs_std'])} | "
        f"{int(r['time_mean'])}±{int(r['time_std'])}"
    )
