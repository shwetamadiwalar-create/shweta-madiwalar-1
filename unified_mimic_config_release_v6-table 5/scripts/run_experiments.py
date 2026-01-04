
import json, os
import torch
from torch.utils.data import DataLoader, TensorDataset
from models.model_definition import get_model
from mimic_loader import load_mimic_dataset

def main():
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configs")
    configs = [f for f in os.listdir(config_dir) if f.endswith(".json")]

    X, y = load_mimic_dataset("path/to/mimic")

    loader = DataLoader(TensorDataset(X, y), batch_size=32, shuffle=True)

    for cfg_file in configs:
        cfg_path = os.path.join(config_dir, cfg_file)
        cfg = json.load(open(cfg_path))

        print(f"Running: {cfg['method']}")

        model = get_model()
        optim = torch.optim.Adam(model.parameters(), lr=1e-3)
        loss_fn = torch.nn.BCEWithLogitsLoss()

        for epoch in range(2):
            for xb, yb in loader:
                optim.zero_grad()
                pred = model(xb)
                loss = loss_fn(pred, yb)
                loss.backward()
                optim.step()
        print("Done.")

if __name__ == "__main__":
    main()
