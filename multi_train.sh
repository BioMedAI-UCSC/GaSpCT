DATA_DIR="../multinerf/chest_xrays/"

# 88/12 train/test split
python train.py -s ${DATA_DIR} -test_holdout 8 --eval --use_yaml
# 83/17 train/test split
python train.py -s ${DATA_DIR} -test_holdout 6 --eval --use_yaml
# 80/20 train/test split
python train.py -s ${DATA_DIR} -test_holdout 5 --eval --use_yaml
# 75/25 train/test split
python train.py -s ${DATA_DIR} -test_holdout 4 --eval --use_yaml
# 33/66 train/test split
python train.py -s ${DATA_DIR} -test_holdout 3 --eval --use_yaml
# 50/50 train/test split
python train.py -s ${DATA_DIR} -test_holdout 2 --eval --use_yaml
# 25/75 train/test split
python train.py -s ${DATA_DIR} -test_holdout -4 --eval --use_yaml
# 10/90 train/test split
python train.py -s ${DATA_DIR} -test_holdout -10 --eval --use_yaml


