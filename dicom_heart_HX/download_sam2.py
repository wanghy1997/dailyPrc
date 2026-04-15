# Using huggingface_hub
from huggingface_hub import hf_hub_download

# Download the recommended latest model
model_path = hf_hub_download(repo_id="wanglab/MedSAM2", filename="MedSAM2_latest.pt")