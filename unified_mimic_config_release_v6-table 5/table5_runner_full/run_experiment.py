
import torch
from dataset import load_dataset, split_clients
from model import Model
from client import Client
from server import Server
from attacks import choose_malicious
from blockchain import consensus_delay
from config import *

X_train, X_test, y_train, y_test = load_dataset()
splits = split_clients(X_train, NUM_CLIENTS)

server = Server(Model())
malicious = choose_malicious(NUM_CLIENTS, MALICIOUS_RATIO)

latencies = []
comm_cost = 0

for r in range(ROUNDS):
    updates = []
    for i in range(NUM_CLIENTS):
        model = Model()
        model.load_state_dict(server.model.state_dict())
        idx = splits[i]
        X = torch.tensor(X_train[idx], dtype=torch.float32)
        y = torch.tensor(y_train[idx], dtype=torch.float32)
        client = Client(model, X, y, malicious=(i in malicious))
        updates.append(client.train())
        comm_cost += sum(p.numel() for p in model.parameters()) * 4 / 1e6
    server.aggregate(updates)
    latencies.append(consensus_delay())

print("Finished Experiment")
print("Communication Cost (MB):", round(comm_cost, 2))
print("Worst-case latency:", (min(latencies), max(latencies)))
