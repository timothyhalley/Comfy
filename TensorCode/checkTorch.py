import torch

print("Cuda Support: ", torch.cuda.is_available())
print("Torch Version: ", (torch.__version__))
print("MPS backend: ", torch.backends.mps.is_available())
