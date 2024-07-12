#!/bin/bash

# this script assumes we have a directory of multiple simulations with images and text files with projection matrices
# it will create a new directory for each simulation and run the train.py script with different test_holdout values
# it will then render the results and calculate the metrics for each simulation

echo "Starting scipt..."

prefix_var="ablation_"
prefix_dir="sims/"
input_yaml="camera_parameters.yml"
output_yaml="cam_config.yaml"
listVar="simulation_0 simulation_1 simulation_2 simulation_3 simulation_4 simulation_5 simulation_6 simulation_7 simulation_8 \
         simulation_9 simulation_10 simulation_11 simulation_12 simulation_13 simulation_14 simulation_15 simulation_16 \
         simulation_17 simulation_18 simulation_19"
test_holdout_list="2"

feature_lr=0.01
opacity_lr=0.01
percent_dense=0.005
lambda_dssim=0.9
lambda_tv="0.005"
lambda_beta="0.005"
ellipsoid="1"
iterations=20000

for ellipse in $ellipsoid; do
    for lam_tv in $lambda_tv; do
        for lam_b in $lambda_beta; do
            if [ "$(echo "$lam_tv == 0" | bc)" -eq 1 ] && [ "$(echo "$lam_b == 0" | bc)" -eq 1 ] && [ "$(echo "$ellipse == 0" | bc)" -eq 1 ]; then
                echo "Skipping already computed case"
            elif [ "$(echo "$lam_tv == 0.005" | bc)" -eq 1 ] && [ "$(echo "$lam_b == 0.005" | bc)" -eq 1 ] && [ "$(echo "$ellipse == 1" | bc)" -eq 1 ]; then
                echo "Skipping already computed case"
            elif [ "$(echo "$lam_tv == 0" | bc)" -eq 1 ] && [ "$(echo "$lam_b == 0.005" | bc)" -eq 1 ] && [ "$(echo "$ellipse == 1" | bc)" -eq 1 ]; then
                echo "Skipping already computed case"
            elif [ "$(echo "$lam_tv == 0.005" | bc)" -eq 1 ] && [ "$(echo "$lam_b == 0" | bc)" -eq 1 ] && [ "$(echo "$ellipse == 1" | bc)" -eq 1 ]; then
                echo "Skipping already computed case"
            else
                echo "Processing Lambda TV $lam_tv, Lambda Beta $lam_b, Ellipsoid Prior $ellipse"
                for i in $listVar; do
                    echo "Processing $i"
                    mkdir -p output/${prefix_var}${i}_ltv${lam_tv}_lb${lam_b}_ellipsoid${ellipse}/sparse/0 output/${prefix_var}${i}_ltv${lam_tv}_lb${lam_b}_ellipsoid${ellipse}/images
                    cp utils/sims/${i}/$input_yaml output/${prefix_var}${i}_ltv${lam_tv}_lb${lam_b}_ellipsoid${ellipse}"/sparse/0/"$output_yaml
                    # maybe we need to convert to rgb from grayscale
                    cp utils/"${prefix_dir}${i}"/*.png "output/${prefix_var}${i}_ltv${lam_tv}_lb${lam_b}_ellipsoid${ellipse}/images/"
                    python utils/rename_images.py -i "output/${prefix_var}${i}_ltv${lam_tv}_lb${lam_b}_ellipsoid${ellipse}/images/"
                    python utils/from_g_to_rgb.py -i "output/${prefix_var}${i}_ltv${lam_tv}_lb${lam_b}_ellipsoid${ellipse}/images/"
                    for j in $test_holdout_list; do
                        echo "Holding every ${j}nd image out for testing..."
                        output_name=output/${prefix_var}${i}_ltv${lam_tv}_lb${lam_b}_ellipsoid${ellipse}/ratio${j}
                        mkdir -p ${output_name}
                        python train.py -s output/${prefix_var}${i}_ltv${lam_tv}_lb${lam_b}_ellipsoid${ellipse} --test_holdout $j --eval --use_yaml --name ${prefix_var}${i}_ltv${lam_tv}_lb${lam_b}_ellipsoid${ellipse}/ratio${j} --iterations $iterations --feature_lr $feature_lr --opacity_lr $opacity_lr --percent_dense $percent_dense --lambda_dssim $lambda_dssim --lambda_tv $lam_tv --lambda_beta $lam_b --ellipsoid $ellipse > $output_name"/train.txt"
                        python render.py -m $output_name > $output_name"/render.txt"
                        python metrics.py -m $output_name > $output_name"/metrics.txt"
                    done
                done
            fi
        done
    done
done

echo "All done..."
