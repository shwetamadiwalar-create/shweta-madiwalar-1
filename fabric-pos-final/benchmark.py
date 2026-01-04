import time
import json
import hashlib
import random
import requests
import statistics
from datetime import datetime

# -----------------------------
# Deterministic configuration
# -----------------------------
SEED = 42
NUM_TRANSACTIONS = 100
TX_PAYLOAD_SIZE = 1024          # bytes (simulated FL update hash)
VALIDATOR_ENDPOINT = "http://localhost:8080/validate"
FABRIC_GATEWAY = "http://localhost:4000/submit"
RESULT_FILE = "benchmark_results.json"

random.seed(SEED)

# -----------------------------
# Utility functions
# -----------------------------
def generate_model_update(tx_id: int):
    """
    Generate a deterministic pseudo FL model update.
    """
    payload = {
        "tx_id": tx_id,
        "timestamp": tx_id,  # deterministic logical time
        "model_hash": hashlib.sha256(
            f"model_update_{tx_id}".encode()
        ).hexdigest(),
        "payload": "0" * TX_PAYLOAD_SIZE
    }
    return payload


def submit_to_validator(tx):
    """
    Submit transaction to external PoS–BFT validator layer.
    """
    response = requests.post(
        VALIDATOR_ENDPOINT,
        json=tx,
        timeout=5
    )
    return response.status_code == 200


def submit_to_fabric(tx):
    """
    Submit approved transaction to Fabric via SDK gateway.
    """
    response = requests.post(
        FABRIC_GATEWAY,
        json=tx,
        timeout=5
    )
    return response.status_code == 200


# -----------------------------
# Benchmark execution
# -----------------------------
latencies = []
accepted = 0
rejected = 0
start_time = time.time()

for i in range(NUM_TRANSACTIONS):
    tx = generate_model_update(i)

    t0 = time.time()
    validator_ok = submit_to_validator(tx)

    if not validator_ok:
        rejected += 1
        continue

    fabric_ok = submit_to_fabric(tx)
    t1 = time.time()

    if fabric_ok:
        accepted += 1
        latencies.append((t1 - t0) * 1000)  # ms
    else:
        rejected += 1

end_time = time.time()

# -----------------------------
# Metrics
# -----------------------------
total_time = end_time - start_time
throughput = accepted / total_time if total_time > 0 else 0

results = {
    "benchmark_time": datetime.utcnow().isoformat(),
    "seed": SEED,
    "num_transactions": NUM_TRANSACTIONS,
    "accepted": accepted,
    "rejected": rejected,
    "throughput_tx_per_sec": throughput,
    "latency_ms": {
        "mean": statistics.mean(latencies) if latencies else 0,
        "median": statistics.median(latencies) if latencies else 0,
        "p95": statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else 0,
        "max": max(latencies) if latencies else 0
    }
}

# -----------------------------
# Save results
# -----------------------------
with open(RESULT_FILE, "w") as f:
    json.dump(results, f, indent=2)

print("Benchmark completed")
print(json.dumps(results, indent=2))
