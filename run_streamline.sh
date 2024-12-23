#!/bin/bash

# This script assumes we have a directory of multiple simulations with images and text files with projection matrices
# It will create a new directory for each simulation and run the train.py script with different test_holdout values
# It will then render the results and calculate the metrics for each simulation

echo "Starting scipt..."

prefix_var="medical_gaspct_"
prefix_dir="data/"
suffix_output="_output"
ct_config_yaml="ct_configuration.yml"
input_yaml="cam_config.yaml"

# List of directories under ./data with radiograph images, can be multiple directories separated by space
data_paths="simulation_0"
# One out of how many pictures should be saved for testing, negatives indicate more testing than training
# In the example below, 1 out of 2 images are hidden from the optimization for testing purposes
# A minus can be used if you want more testing data than training data. "-4" means 1 out of 4 images is used for training the model.
# Multiple ratios can be passed separated by space
test_holdout_list="2"

# Hyperparameters related to the training of the model
feature_lr=0.01
opacity_lr=0.01
percent_dense=0.005
lambda_dssim=0.9
lambda_tv=0.005
lambda_beta=0.005
iterations=25000

# Multiple tests for different data paths
for i in $data_paths; do
    echo "Processing $i"
    mkdir -p output/${prefix_var}${i}/sparse/0 output/${prefix_var}${i}/images
    python utils/camera_generator.py -i "${prefix_dir}${i}"/$ct_config_yaml -o "${prefix_dir}${i}"/$input_yaml
    cp "${prefix_dir}${i}"/$input_yaml output/$prefix_var$i"/sparse/0/"
    cp "${prefix_dir}${i}"/*.png "output/${prefix_var}${i}/images/"
    # In case images need to be renamed and converted to rgb from grayscale (TODO: confirm naming works well)
    python utils/rename_images.py -i "output/${prefix_var}${i}/images/"
    python utils/from_g_to_rgb.py -i "output/${prefix_var}${i}/images/"
    # Multiple tests for different training to testing ratios
    for j in $test_holdout_list; do
        echo "Holding every ${j}th image out for testing..."
        output_name=output/${prefix_var}${i}/ratio${j}
	    mkdir -p ${output_name}
        python train.py -s output/$prefix_var$i --test_holdout $j --eval --use_yaml --name ${prefix_var}${i}/ratio${j} --iterations $iterations --feature_lr $feature_lr --opacity_lr $opacity_lr --percent_dense $percent_dense --lambda_dssim $lambda_dssim --lambda_tv $lambda_tv --lambda_beta $lambda_beta > $output_name"/train.txt"
        python render.py -m $output_name > $output_name"/render.txt"
        python metrics.py -m $output_name > $output_name"/metrics.txt"
    done
done

echo "All done..."
