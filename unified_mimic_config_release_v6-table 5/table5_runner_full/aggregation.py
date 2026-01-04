
def fedavg(updates):
    agg = {}
    for k in updates[0]:
        agg[k] = sum(u[k] for u in updates) / len(updates)
    return agg
