#!/bin/bash

echo "Creating and activating Conda environment..."
conda activate osbridgelcca || conda create -n osbridgelcca python=3.9 -y && conda activate osbridgelcca

echo "Installing dependencies from pyproject.toml..."
pip install .

echo "Installation complete!"
python scripts/verify_installation.py
