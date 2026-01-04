import time, json
from hfc.fabric import Client

TX_COUNTS = [500, 1000, 2500, 5000, 10000]
PAYLOAD_SIZES = [1024, 4096, 10240]  # bytes

client = Client(net_profile="network.json")

def submit(tx_count, payload_size):
    payload = "x" * payload_size
    start = time.time()

    for _ in range(tx_count):
        client.chaincode_invoke(
            requestor="Admin",
            channel_name="benchmark",
            cc_name="fl_cc",
            fcn="SubmitUpdate",
            args=[payload],
            wait_for_event=True
        )

    end = time.time()
    return {
        "tx": tx_count,
        "payload": payload_size,
        "latency": (end - start) / tx_count
    }

results = []
for tx in TX_COUNTS:
    for ps in PAYLOAD_SIZES:
        results.append(submit(tx, ps))

json.dump(results, open("results.json", "w"), indent=2)
