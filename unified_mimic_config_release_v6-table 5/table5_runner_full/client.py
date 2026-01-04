
import torch
from torch.optim import Adam
from config import LOCAL_EPOCHS, LR

class Client:
    def __init__(self, model, X, y, malicious=False):
        self.model = model
        self.X = X
        self.y = y
        self.malicious = malicious
        self.opt = Adam(self.model.parameters(), lr=LR)

    def train(self):
        self.model.train()
        for _ in range(LOCAL_EPOCHS):
            pred = self.model(self.X).squeeze()
            loss = torch.nn.functional.binary_cross_entropy(pred, self.y.float())
            self.opt.zero_grad()
            loss.backward()
            if self.malicious:
                for p in self.model.parameters():
                    p.grad *= -3
            self.opt.step()
        return {k: v.detach().clone() for k, v in self.model.state_dict().items()}
