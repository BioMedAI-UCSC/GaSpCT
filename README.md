# GaSpCT: Gaussian splatting for novel brain CBCT projection view synthesis

## Overview
GaSpCT is an adaptation of Gaussian Splatting specifically designed for sparse-view Cone Beam Computed Tomography (CBCT) projection images. This project extends the original work by INRIA to handle medical imaging applications.
Our main contributions include:
- A framework to extract camera intrinsics and extrinsics using scanner metadata
- An enhanced loss function that better captures the characteristics of radiographs
- An ellipsoid point initialization
- A validation that Gaussian Splatting represents a robust and accurate methodology for radiograph synthesis in sparse-view CBCT

## Original Work
This repository is heavily based on the Gaussian Splatting repository by INRIA:
- [Original Repository](https://github.com/graphdeco-inria/gaussian-splatting)
- [Research Paper](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/3d_gaussian_splatting_high.pdf)

## Project Status
This project has been accepted for a poster presentation in SPIE Medical Imaging 2025, in San Diego


### Main Contributors
- Emmanouil "Manolis" Nikolakakis
- Utkarsh Gupta
- Jonathan Vengosh
- Justin Bui

### Faculty Advisor
- Professor Razvan Marinescu

### Institution
University of California, Santa Cruz

---
### Running the code

# Cloning the Repository

The repository contains submodules, thus please check it out with

```bash
# SSH
git clone git@github.com:BioMedAI-UCSC/GaSpCT.git --recursive
```
or

```bash
# HTTPS
git clone https://github.com/BioMedAI-UCSC/GaSpCT.git --recursive
```

# Installing requirements

# Installing the submodules

# Setting up the directory

# Training, rendering and evaluating the gaussian splatting scene representation

# BibTex

If you have used our work or found it insightful for your project, please consider citing us using the following BibTex block

@article{nikolakakis2024gaspct,
  title={GaSpCT: Gaussian Splatting for Novel CT Projection View Synthesis},
  author={Nikolakakis, Emmanouil and Gupta, Utkarsh and Vengosh, Jonathan and Bui, Justin and Marinescu, Razvan},
  journal={arXiv preprint arXiv:2404.03126},
  year={2024}
}
