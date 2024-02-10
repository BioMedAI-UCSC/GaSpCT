#!/bin/bash

# this script assumes we have a directory of multiple simulations with images and text files with projection matrices
# it will create a new directory for each simulation and run the train.py script with different test_holdout values
# it will then render the results and calculate the metrics for each simulation

echo "Starting scipt..."

prefix_var="medical_"
prefix_dir="sims/"
suffix_output="_output"
output_yaml="cam_config.yml"
listVar="simulation_1 simulation_2 simulation_3 simulation 4 simulation 5 simulation 6 simulation 7 simulation 8 \
         simulation_9 simulation_10 simulation_11 simulation 12 simulation 13 simulation 14 simulation 15 simulation 16 \
         simulation_17 simulation 18 simulation 19"
test_holdout_list="10 5 4 2 -4 -10"
for i in $listVar; do
    echo "Processing $i"
    cd utils
    python projection_text_to_yaml.py -i $prefix_dir$i -o $output_yaml
    cd ..
    mkdir $prefix_var$i
    cd $prefix_var$i
    mkdir images
    mkdir sparse
    cd sparse
    mkdir 0
    cd ../../
    mv utils/$output_yaml $prefix_var$i"/sparse/0/"$output_yaml 
    # maybe we need to convert to rgb from grayscale
    cp utils/"${prefix_dir}${i}"/*.png "${prefix_var}${i}/images/"
    for j in $test_holdout_list; do
        echo "Holding every $jth image out for testing..."
        output_name=$prefix_var$i"/ratio_"$j
        python train.py -s $prefix_var$i --test_holdout $j --eval --use_yaml --name $output_name --iterations 35000 > $output_name"_train.txt"
        python render.py -m $output_name > $output_name"_render.txt"
        python metrics.py -m $output_name > $output_name"_metrics.txt"
    done
done

echo "All done..."
