
import random

def choose_malicious(n_clients, ratio):
    n = int(n_clients * ratio)
    return set(random.sample(range(n_clients), n))
