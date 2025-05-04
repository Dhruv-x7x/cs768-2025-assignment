"""
Downloads dataset via gdown, extracts it, then runs generate_graph.py using subprocess.run
Requires: gdown, tarfile, subprocess, os
"""
import os
import subprocess
import tarfile

# Try importing gdown, else prompt user to install
try:
    import gdown
except ImportError:
    print("ERROR: gdown not installed. Run: pip install gdown")
    exit(1)

# Google Drive file ID to use in gdown. Learn how to use it at https://pypi.org/project/gdown/
FILE_ID = "1J73io_KqCoPEAlH3teLWGoZ78yk5n7ll"
DATA_ARCHIVE = "dataset_papers.tar.gz"
DATA_DIR = "dataset_papers"

# Only download dataset if not present
if not os.path.exists(DATA_ARCHIVE):
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    print(f"Downloading dataset to {DATA_ARCHIVE}...")
    gdown.download(url, DATA_ARCHIVE, quiet=False)
else:
    print(f"Found existing archive {DATA_ARCHIVE}, skipping download.")

# Only extract archive if not already extracted. Learn how to use tarfile at https://docs.python.org/3/library/tarfile.html
if not os.path.isdir(DATA_DIR):
    print(f"Extracting {DATA_ARCHIVE} to {DATA_DIR}/...")
    with tarfile.open(DATA_ARCHIVE, "r:gz") as tar: # don't forget r:gz as we are working with a gzipped tar file
        tar.extractall()
else:
    print(f"Found existing directory {DATA_DIR}, skipping extraction.")

# Run generate_graph.py
print("Running generate_graph.py on the dataset...")
subprocess.run([
    "python", "generate_graph.py", "--dataset-path", DATA_DIR
], check=True)
print("Task1 complete.")
