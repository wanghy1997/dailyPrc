import torch
import torch.nn as nn


class AttentionGate(nn.Module):
    def __init__(self, F_g=3, F_l=3, F_int=1, **kwargs):
        super().__init__()
        self.W_g = nn.Sequential(
            nn.Conv2d(3, 1, 1, 1),
            nn.BatchNorm2d(1)
        )

        self.W_x = nn.Sequential(
            nn.Conv2d(3, 1, 1, 2),
            nn.BatchNorm2d(1)
        )

        self.psi = nn.Sequential(
            nn.Conv2d(1, 1, 1, 1),
            nn.Sigmoid()
        )

        self.upsample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False)

        self.relu = nn.ReLU(inplace=True)

    def forward(self, g, x):
        g1 = self.W_g(g)
        x1 = self.W_x(x)
        o = g1 + x1
        psi = self.relu(o)
        psi = self.psi(psi)
        psi_up = self.upsample(psi)
        out = x * psi_up
        return out


if __name__ == '__main__':
    g = torch.randn(1, 3, 56, 56)
    x = torch.randn(1, 3, 112, 112)
    model = AttentionGate()
    y = model(g, x)
    print(y.size())
