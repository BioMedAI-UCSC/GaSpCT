#!/bin/bash

# this script assumes we have a directory of multiple simulations with images and text files with projection matrices
# it will create a new directory for each simulation and run the train.py script with different test_holdout values
# it will then render the results and calculate the metrics for each simulation

echo "Starting scipt..."

prefix_var="medical_gaspct_default_loss_"
prefix_dir="sims/"
suffix_output="_output"
output_yaml="cam_config.yaml"
listVar="simulation_0 simulation_1 simulation_2 simulation_3 simulation_4 simulation_5 simulation_6 simulation_7 simulation_8 \
         simulation_9 simulation_10 simulation_11 simulation_12 simulation_13 simulation_14 simulation_15 simulation_16 \
         simulation_17 simulation_18 simulation_19"
test_holdout_list="10 5 4 2 -4 -10"

feature_lr=0.01
opacity_lr=0.01
percent_dense=0.005
lambda_dssim=0.9
lambda_tv=0.005
lambda_beta=0.005
iterations=35000

for i in $listVar; do
    echo "Processing $i"
    cd utils
    python projection_text_to_yaml.py -i $prefix_dir$i -o $output_yaml
    cd ..
    mkdir -p output/${prefix_var}${i}/sparse/0 output/${prefix_var}${i}/images
    mv utils/$output_yaml output/$prefix_var$i"/sparse/0/"$output_yaml
    # maybe we need to convert to rgb from grayscale
    cp utils/"${prefix_dir}${i}"/*.png "output/${prefix_var}${i}/images/"
    python utils/rename_images.py -i "output/${prefix_var}${i}/images/"
    python utils/from_g_to_rgb.py -i "output/${prefix_var}${i}/images/"
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
