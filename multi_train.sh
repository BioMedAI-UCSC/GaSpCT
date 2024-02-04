DATA_DIR="../multinerf/chest_xrays/"

# 88/12 train/test split
python train.py -s ${DATA_DIR} -test_holdout 8 --eval --use_yaml --name 88-12 --iterations 20000
# 83/17 train/test split
python train.py -s ${DATA_DIR} -test_holdout 6 --eval --use_yaml --name 83-17 --iterations 20000
# 80/20 train/test split
python train.py -s ${DATA_DIR} -test_holdout 5 --eval --use_yaml --name 80-20 --iterations 20000
# 75/25 train/test split
python train.py -s ${DATA_DIR} -test_holdout 4 --eval --use_yaml --name 75-25 --iterations 20000
# 66/33 train/test split
python train.py -s ${DATA_DIR} -test_holdout 3 --eval --use_yaml --name 66-33 --iterations 20000
# 50/50 train/test split
python train.py -s ${DATA_DIR} -test_holdout 2 --eval --use_yaml --name 50-50 --iterations 20000
# 25/75 train/test split
python train.py -s ${DATA_DIR} -test_holdout -4 --eval --use_yaml --name 25-75 --iterations 20000
# 10/90 train/test split
python train.py -s ${DATA_DIR} -test_holdout -10 --eval --use_yaml --name 10-90 --iterations 20000


