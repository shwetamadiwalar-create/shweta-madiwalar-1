import json, random

def pos_select(stake_table, k=3):
    peers = list(stake_table.keys())
    stakes = [stake_table[p] for p in peers]
    selected = random.choices(peers, weights=stakes, k=k)
    return list(set(selected))

if __name__ == "__main__":
    stake_table = {"Org1":10, "Org2":10}
    validators = pos_select(stake_table)
    with open("config/validators_epoch_0.json","w") as f:
        json.dump(validators, f)
