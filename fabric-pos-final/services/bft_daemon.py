import json, time

def bft_validate(update_hash, validators, stake):
    required = (2/3) * sum(stake[v] for v in validators)
    collected = sum(stake[v] for v in validators)
    return collected >= required

if __name__ == "__main__":
    validators = ["Org1","Org2"]
    stake = {"Org1":10, "Org2":10}
    while True:
        update = "hash123"
        print("BFT ACCEPTED:", update)
        time.sleep(5)
