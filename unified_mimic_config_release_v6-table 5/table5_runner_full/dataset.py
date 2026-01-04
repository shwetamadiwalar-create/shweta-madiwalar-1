
import numpy as np
from sklearn.model_selection import train_test_split

def load_dataset():
    X = np.random.randn(2000, 20)
    y = np.random.randint(0, 2, 2000)
    return train_test_split(X, y, test_size=0.2, random_state=42)

def split_clients(X, n_clients):
    idx = np.array_split(np.arange(len(X)), n_clients)
    return idx
