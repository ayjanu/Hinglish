"""
Dataset Manager for HinglishVinglish
Downloads and manages the English-Hindi translation dataset from Kaggle
"""

import os
import pandas as pd
from pathlib import Path


class DatasetManager:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.english_to_hindi = {}
        self.hindi_to_english = {}

    def download_dataset(self):
        """Download dataset from Kaggle using kagglehub"""
        try:
            import kagglehub
            print("Downloading dataset from Kaggle...")
            path = kagglehub.dataset_download('preetviradiya/english-hindi-dataset')
            print(f"Dataset downloaded to {path}")
            return path
        except Exception as e:
            print(f"Error downloading dataset: {e}")
            print("Please ensure you have:")
            print("1. A Kaggle account")
            print("2. API credentials in ~/.kaggle/kaggle.json")
            raise

    def load_dataset(self):
        """Load and parse the dataset into memory"""
        # Check if dataset exists, if not download it
        dataset_files = list(self.data_dir.glob("*.csv")) + list(self.data_dir.glob("*.txt"))

        if not dataset_files:
            print("Dataset not found. Downloading...")
            downloaded_path = self.download_dataset()
            # kagglehub downloads to its own cache, so search there
            downloaded_path = Path(downloaded_path)
            dataset_files = list(downloaded_path.glob("*.csv")) + list(downloaded_path.glob("*.txt"))
            # If found, update our search path
            if dataset_files:
                self.data_dir = downloaded_path
            else:
                # Fall back to checking our data dir
                dataset_files = list(self.data_dir.glob("*.csv")) + list(self.data_dir.glob("*.txt"))

        if not dataset_files:
            raise FileNotFoundError("No dataset files found after download")

        # Load the dataset
        print(f"Loading dataset from {dataset_files[0]}...")

        try:
            # Try loading as CSV
            df = pd.read_csv(dataset_files[0])

            # Detect column names (common variations)
            english_col = None
            hindi_col = None

            for col in df.columns:
                col_lower = col.lower()
                if 'english' in col_lower or 'en' in col_lower:
                    english_col = col
                elif 'hindi' in col_lower or 'hi' in col_lower:
                    hindi_col = col

            if not english_col or not hindi_col:
                # If columns not detected, use first two columns
                cols = df.columns.tolist()
                if len(cols) >= 2:
                    english_col, hindi_col = cols[0], cols[1]
                else:
                    raise ValueError("Could not identify English and Hindi columns")

            print(f"Using columns: {english_col} (English), {hindi_col} (Hindi)")

            # Build bidirectional dictionaries
            for _, row in df.iterrows():
                english = str(row[english_col]).strip()
                hindi = str(row[hindi_col]).strip()

                if english and hindi and english != 'nan' and hindi != 'nan':
                    # Store with case normalization for lookup
                    self.english_to_hindi[english.lower()] = hindi
                    self.hindi_to_english[hindi] = english

            print(f"Loaded {len(self.english_to_hindi)} translation pairs")

        except Exception as e:
            print(f"Error loading dataset: {e}")
            raise

    def get_hindi_translation(self, english_text):
        """Get Hindi translation for English text"""
        return self.english_to_hindi.get(english_text.lower())

    def get_english_translation(self, hindi_text):
        """Get English translation for Hindi text"""
        return self.hindi_to_english.get(hindi_text)


if __name__ == "__main__":
    # Test the dataset manager
    manager = DatasetManager()
    manager.load_dataset()
    print("\nDataset loaded successfully!")
    print(f"Total English→Hindi pairs: {len(manager.english_to_hindi)}")
    print(f"Total Hindi→English pairs: {len(manager.hindi_to_english)}")
