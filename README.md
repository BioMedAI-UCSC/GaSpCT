# GaSpCT: Gaussian splatting for novel brain CBCT projection view synthesis

## Overview
GaSpCT is an adaptation of Gaussian Splatting specifically designed for sparse-view Cone Beam Computed Tomography (CBCT) projection images. This project extends the original work by INRIA to handle medical imaging applications.
Our main contributions include:
- A framework to extract camera intrinsics and extrinsics using scanner metadata
- An enhanced loss function that better captures the characteristics of radiographs
- An ellipsoid point initialization
- A validation that Gaussian Splatting represents a robust and accurate methodology for radiograph synthesis in sparse-view CBCT

## Original Work
This repository is heavily based on the Gaussian Splatting repository by INRIA, our work wouldn't be possible without it:
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

The repository contains submodules, thus please check it out with:

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
```bash
# You can use conda to install the python packages and install the required submodules using the appropriate channels
conda env create -f environment.yml
```

# Setting up the directory

To run GaSpCT, please copy your radiograph image dataset in ./data and update the ct_configuration.yml file with the scanner data of the CT scan.
If you would like to generate radiographs from a 3D DICOM or MHA volume, please use the script: ./utils/generate_drr_gaspct (you will need to have plastimatch installed for this): https://plastimatch.org/getting_started.html

# Training, rendering and evaluating the gaussian splatting scene representation

We recommend using our streamline shell script to run GaSpCT which should take care of everything:

```bash
./run_streamline.sh
```

You can edit "data_paths" if you want to generate results for one or multiple set of radiographs. Also you might want to change "test_holdout_list" to run GaSpCT for one or more ratios of training / testing data points.
Your generated point cloud will be found under: ./output/"name of run"/"testing-training ratio"
You can also find rendered images versus the ground truth under: ./output/"name of run"/"testing-training ratio/test"
Moreover, you can find the metrics.txt file under: ./output/"name of run"/"testing-training ratio
Finally, you might find our "./utils/ablation_metric_extractor.py" script helpful. It was used to get the average metric results for various tests when we were doing our ablation studies.

# BibTex

If you have used our work or found it insightful for your project, please consider citing us using the following BibTex block

@article{nikolakakis2024gaspct,
  title={GaSpCT: Gaussian Splatting for Novel CT Projection View Synthesis},
  author={Nikolakakis, Emmanouil and Gupta, Utkarsh and Vengosh, Jonathan and Bui, Justin and Marinescu, Razvan},
  journal={arXiv preprint arXiv:2404.03126},
  year={2024}
}
