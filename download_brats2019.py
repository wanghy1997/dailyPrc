import kagglehub

# Download latest version
path = kagglehub.dataset_download("aryashah2k/brain-tumor-segmentation-brats-2019")

print("Path to dataset files:", path)