from torch.utils.data import DataLoader, TensorDataset
import torch

# Suppose you have some data in the form of PyTorch tensors
features = torch.randn(100, 10)  # 100 samples, 10 features each
labels = torch.randint(0, 2, (100,))  # 100 labels, either 0 or 1

# You can create a TensorDataset from your data
dataset = TensorDataset(features, labels)

# And then create a DataLoader from your dataset
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
