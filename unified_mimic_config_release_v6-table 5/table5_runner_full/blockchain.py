
import random
from config import BLOCKCHAIN_LATENCY

def consensus_delay(mode="PoS_BFT"):
    lo, hi = BLOCKCHAIN_LATENCY[mode]
    return random.uniform(lo, hi)
