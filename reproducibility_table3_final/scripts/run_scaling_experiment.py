import yaml
import csv
from train_federated import train_model

with open("configs/experiment.yaml") as f:
    cfg = yaml.safe_load(f)

results = []

for nodes in cfg["edge_nodes"]:
    for run in range(cfg["num_runs"]):
        metrics = train_model(
            num_clients=nodes,
            max_epochs=cfg["training"]["max_epochs"],
            delta=cfg["training"]["convergence_delta"],
            seed=cfg["seed"] + run
        )
        metrics["nodes"] = nodes
        results.append(metrics)

with open(cfg["output"]["raw_results"], "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Scaling experiment completed successfully")
