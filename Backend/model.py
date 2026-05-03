import torch
import torch.nn as nn
import torch.nn.functional as F

class AutismPredictor:
    def __init__(self):
        # Simple linear layer: 15 inputs → 1 output
        self.net = nn.Linear(15, 1)
        # Fix random seed for reproducibility
        torch.manual_seed(42)
        # Initialize weights (default torch init) – no training data, so they stay random
        for p in self.net.parameters():
            if p.requires_grad:
                nn.init.normal_(p, mean=0.0, std=0.5)
        self.net.eval()

    def predict(self, answers: list[int]) -> float:
        """Predict probability of autism from a list of 15 integer answers (0‑3)."""
        # Convert list of 0‑3 scores to tensor of shape (1,15)
        x = torch.tensor(answers, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            logit = self.net(x)
            prob = torch.sigmoid(logit).item()
        return prob

        
