import kagglehub

# Download latest version
path = kagglehub.dataset_download("preetviradiya/english-hindi-dataset")

print("Path to dataset files:", path)