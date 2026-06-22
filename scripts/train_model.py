"""Standalone script to train and save the churn model."""
import sys
sys.path.insert(0, "/app")
from app.ml.pipeline import train

if __name__ == "__main__":
    train()
