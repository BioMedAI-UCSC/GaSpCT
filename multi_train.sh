DATA_DIR="../multinerf/chest_xrays/"

# 88/12 train/test split
python train.py -s ${DATA_DIR} -test_holdout 8 --eval
# 83/17 train/test split
python train.py -s ${DATA_DIR} -test_holdout 6 --eval
# 80/20 train/test split
python train.py -s ${DATA_DIR} -test_holdout 5 --eval
# 75/25 train/test split
python train.py -s ${DATA_DIR} -test_holdout 4 --eval
# 33/66 train/test split
python train.py -s ${DATA_DIR} -test_holdout 3 --eval
# 50/50 train/test split
python train.py -s ${DATA_DIR} -test_holdout 2 --eval
# 25/75 train/test split
python train.py -s ${DATA_DIR} -test_holdout -4 --eval
# 10/90 train/test split
python train.py -s ${DATA_DIR} -test_holdout -10 --eval


