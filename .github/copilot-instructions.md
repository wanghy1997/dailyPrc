# Copilot Instructions for This Codebase

Welcome to the codebase! This document provides essential guidance for AI coding agents to be productive and aligned with the project's structure, conventions, and workflows.

## Big Picture Overview

This repository appears to be a collection of Python scripts and utilities, organized by functionality and date. Key components include:

- **Data Processing**: Scripts like `add_imags_segmentationResults.py`, `changePDF.py`, and `comFile.py` handle various data manipulation tasks.
- **Visualization**: Files such as `viz_Axial_2d.py`, `viz_mask.py`, and `viz_qumian.py` focus on generating visual outputs.
- **Medical Imaging**: Directories like `dicom_heart_HX/` and `liweikai_dcm2nii/` contain scripts for processing medical imaging data (e.g., DICOM files).
- **Utilities**: The `utils_all/` directory contains helper scripts like `utils_delete_file_with_name.py` for common operations.

### Directory Highlights
- **`2023*/2025*`**: These folders contain dated scripts, likely for specific experiments or tasks.
- **`connect2net/`**: Handles network-related operations.
- **`images/`**: Stores image data, organized into subfolders like `gray/`, `img/`, and `mask/`.

## Developer Workflows

### Running Scripts
Most scripts can be executed directly using Python. For example:
```bash
python add_imags_segmentationResults.py
```

### Debugging
Use `print` statements or Python's built-in `pdb` module for debugging. Example:
```python
import pdb; pdb.set_trace()
```

### Dependencies
Some scripts may rely on external libraries. Ensure you have the required packages installed. Use the following command to install dependencies:
```bash
pip install -r requirements.txt
```
If no `requirements.txt` exists, manually inspect the imports in the scripts.

## Project-Specific Conventions

- **File Naming**: Many files are named with dates (e.g., `py_20240519.py`), indicating their creation or relevance to specific tasks.
- **Visualization Outputs**: Scripts in the `viz_*` files generate visualizations, often saved in the `images/` directory.
- **Medical Imaging**: Follow DICOM processing patterns in `dicom_heart_HX/` and `liweikai_dcm2nii/`.

## Integration Points

- **External Libraries**: Common libraries include `numpy`, `pandas`, and `matplotlib`. Install missing libraries as needed.
- **Data Files**: Ensure required data files (e.g., images, DICOM files) are in the correct directories before running scripts.

## Examples

### Adding a New Visualization Script
1. Place the script in the root directory or a relevant subfolder (e.g., `20240508/`).
2. Follow the naming convention: `viz_<description>.py`.
3. Save outputs to the `images/` directory.

### Processing Medical Images
Refer to `dicom_heart_HX/read_dicom.py` for examples of reading and processing DICOM files.

---

For further clarification or updates, modify this document to reflect new patterns or workflows.