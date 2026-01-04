
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

def evaluate(model, X, y):
    model.eval()
    with np.errstate(all='ignore'):
        preds = model(X).detach().numpy().squeeze()
    y_pred = (preds > 0.5).astype(int)
    return {
        "accuracy": accuracy_score(y, y_pred),
        "f1": f1_score(y, y_pred),
        "auc": roc_auc_score(y, preds)
    }
