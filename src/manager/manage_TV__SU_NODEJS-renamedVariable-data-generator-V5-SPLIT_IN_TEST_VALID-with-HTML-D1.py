import json
import subprocess
from shutil import copy

from src.manager.CreateCode2VecSets import CreateCode2VecSets
from src.manager.manageDataSet import *



logging.basicConfig(format="%(levelname)s - %(asctime)s - %(filename)s/%(funcName)s - line %(lineno)d: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)

########################################################################################################################
###### READ ME TO UNDERSTAND WHAT HAPPEN IN THIS PYTHON SCRIPT IN A SHORT EXPLANATION
# It script is to generate the data in input of the PHP/NODEJS JAVA PARSER creating the set of AST paths to code2vec preprocess
# What you have to change to run this script in order to shuffle and divide on trainset 69%, validationset 30% and testset 1% of the trainset
# is only the config part such as :
# --- the path of the PHP/NodeJs dataset
# --- the path of the new folders where would like put the train + test + valid dataset
# This script is optimized to use threads
########################################################################################################################
###### CONFIG PART
CONST_RULES = '-r0-r1-r2-r5_14'

NUMBER_OF_SAMPLES = 'total'

LANG = 'NODEJS'
LANG = 'HOP'


WITH_R_R_R___ = '%s%s' % (NUMBER_OF_SAMPLES,CONST_RULES )




DATASET_NAME = '%s-renamedVariable-data-%s-template-with-HTML-for-D2' % (LANG, WITH_R_R_R___)
DATASET = '/absolute/path/%s/' % DATASET_NAME #I can used for word2vec like that

# NEW_DATASET_NAME = '%s-final-preprocessed-renamedVariable-data-%s-template_SPLIT_IN_TEST_VALID-with-HTML-D1' % (LANG, WITH_R_R_R___)
NEW_DATASET_NAME = '%s-final-preprocessed-renamedVariable-data-%s-template_SPLIT_IN_TEST_VALID-with-HTML-D2' % (LANG, WITH_R_R_R___)
NEW_DATASET_PATH = '../../../db/db-v1/%s' % NEW_DATASET_NAME
TRAIN_SET_PATH = os.path.join(NEW_DATASET_PATH,'trainset_files/')
TEST_SET_PATH =  os.path.join(NEW_DATASET_PATH,'testset_files/')
VALID_SET_PATH =  os.path.join(NEW_DATASET_PATH,'validset_files/')
JSON_CONFIG_PATH = '../../db-config/db-v1'
JSON_PATH = '%s/%s.json' % (JSON_CONFIG_PATH, NEW_DATASET_NAME)
########################################################################################################################
create_folder_if_not_exist(JSON_CONFIG_PATH)
informationsFiles = retrieve_informations_about_dataset(DATASET)
total_in_dataset = informationsFiles[TOTAL_IN_DATASET]
logging.info("Total of source codes/files in the whole dataset : %d ", total_in_dataset)
total_trainset, total_testset, total_validset = getNumberOfDataInEachSetCustom(total_in_dataset,0,50/100,50/100, withval=True)
logging.info("In the end, Total of source codes/files in the train dataset has to be 69pc: %d", total_trainset)
logging.info("In the end, Total of source codes/files in the test dataset has to be 1pc: %d", total_testset)
logging.info("In the end, Total of source codes/files in the valid dataset has to be 30pc: %d", total_validset)
try :
    assert total_trainset + total_testset + total_validset == total_in_dataset
# logging.info("Information files %s ", informationsFiles)
except Exception as e :
    logging.info("%d + %d + %d = %d and expected %d", total_validset, total_testset, total_trainset, total_trainset + total_testset + total_validset, total_in_dataset )
    raise e
total_safe_files = informationsFiles[SAFE][TOTAL_FILES]
logging.info("Total of source codes/files in the safe dataset : %d", total_safe_files)
total_unsafe_files = informationsFiles[UNSAFE][TOTAL_FILES]
logging.info("Total of source codes/files in the unsafe dataset : %d", total_unsafe_files)
assert total_safe_files + total_unsafe_files  == total_in_dataset

Y_SAFE = getYSet(total_safe_files, SAFE)
logging.info("len Y SAFE : %d", len(Y_SAFE))
assert total_safe_files == len(Y_SAFE)
Y_UNSAFE = getYSet(total_unsafe_files, UNSAFE)
logging.info("len Y UNSAFE : %d", len(Y_UNSAFE))
assert total_unsafe_files == len(Y_UNSAFE)

X_list, Y_list = shuffleDataSet(informationsFiles[SAFE][FILES], Y_SAFE, informationsFiles[UNSAFE][FILES], Y_UNSAFE)
logging.info("number of file in X list shuffled %d",len(X_list))
logging.info("number of file in Y list shuffled %d",len(Y_list))
assert total_in_dataset == len(X_list)
assert total_in_dataset == len(Y_list)
assert  len(X_list) == len(Y_list)

#Divide X shuffled list in 2 : trainX and TestX
X_list_train, X_list_valid, X_list_test = divideDataSet(total_trainset, X_list, withvaliditation=True, totalInValidationSet=total_validset)
logging.info("number of file in X trainset shuffled %d == total in the end %d",len(X_list_train), total_trainset)
logging.info("number of file in X testset shuffled %d == total in the end %d",len(X_list_test), total_testset)
logging.info("number of file in X validset shuffled %d == total in the end %d",len(X_list_valid), total_validset)
assert len(X_list_train) == total_trainset
assert len(X_list_valid) == total_validset
assert len(X_list_test) == total_testset


Y_list_train, Y_list_valid, Y_list_test = divideDataSet(total_trainset, Y_list, withvaliditation=True, totalInValidationSet=total_validset)
logging.info("number of file in Y trainset shuffled %d", len(Y_list_train))
logging.info("number of file in Y testset shuffled %d", len(Y_list_test))
logging.info("number of file in X validset shuffled %d == total in the end %d",len(Y_list_valid), total_validset)
assert len(Y_list_train) == total_trainset
assert len(Y_list_test) == total_testset
assert len(Y_list_valid) == total_validset
assert len(Y_list_train) != len(Y_list_test)

logging.info("NUMBER OF SAFE IN TRAIN SET %s", Y_list_train.count(1))
logging.info("NUMBER OF SAFE IN TEST SET %s", Y_list_test.count(1))
logging.info("NUMBER OF SAFE IN VALID SET %s", Y_list_valid.count(1))
logging.info("NUMBER OF UNSAFE IN TRAIN SET %s", Y_list_train.count(0))
logging.info("NUMBER OF UNSAFE IN TEST SET %s", Y_list_test.count(0))
logging.info("NUMBER OF UNSAFE IN VALID SET %s", Y_list_valid.count(0))
assert Y_list_train.count(0) + Y_list_test.count(0) +  Y_list_valid.count(0) == total_unsafe_files
assert Y_list_train.count(1) + Y_list_test.count(1) + Y_list_valid.count(1)== total_safe_files



TRAIN_SET_SAFE_PATH = os.path.join(TRAIN_SET_PATH, 'safe')
create_folder_if_not_exist(TRAIN_SET_SAFE_PATH)
TRAIN_SET_UNSAFE_PATH = os.path.join(TRAIN_SET_PATH, 'unsafe')
create_folder_if_not_exist(TRAIN_SET_UNSAFE_PATH)
TEST_SET_SAFE_PATH = os.path.join(TEST_SET_PATH, 'safe')
create_folder_if_not_exist(TEST_SET_SAFE_PATH)
TEST_SET_UNSAFE_PATH = os.path.join(TEST_SET_PATH, 'unsafe')
create_folder_if_not_exist(TEST_SET_UNSAFE_PATH)
VALID_SET_SAFE_PATH = os.path.join(VALID_SET_PATH,'safe')
create_folder_if_not_exist(VALID_SET_SAFE_PATH)
VALID_SET_UNSAFE_PATH = os.path.join(VALID_SET_PATH,'unsafe')
create_folder_if_not_exist(VALID_SET_UNSAFE_PATH)


logging.info("Création des threads")
# Création des threads
thread_1 = CreateCode2VecSets(Y_list_train, X_list_train, TRAIN_SET_SAFE_PATH, TRAIN_SET_UNSAFE_PATH)
thread_2 = CreateCode2VecSets(Y_list_test, X_list_test, TEST_SET_SAFE_PATH, TEST_SET_UNSAFE_PATH)
thread_3 = CreateCode2VecSets(Y_list_valid, X_list_valid, VALID_SET_SAFE_PATH, VALID_SET_UNSAFE_PATH)

logging.info("Lancement des threads")
# Lancement des threads
thread_1.start()
thread_2.start()
thread_3.start()

# Attend que les threads se terminent
thread_1.join()
thread_2.join()
thread_3.join()

dict_res = {}
informationsFiles = retrieve_informations_about_dataset(TRAIN_SET_PATH)
logging.info("Total of source codes/files in the whole TRAIN dataset : %d ", informationsFiles[TOTAL_IN_DATASET])
logging.info("Total of source codes/files in the safe TRAIN dataset : %d", informationsFiles[SAFE][TOTAL_FILES])
logging.info("Total of source codes/files in the unsafe TRAIN dataset : %d", informationsFiles[UNSAFE][TOTAL_FILES])
dict_res["trainset_files"] = informationsFiles

informationsFiles = retrieve_informations_about_dataset(TEST_SET_PATH)
logging.info("Total of source codes/files in the whole TEST dataset : %d ", informationsFiles[TOTAL_IN_DATASET])
logging.info("Total of source codes/files in the safe TEST dataset : %d", informationsFiles[SAFE][TOTAL_FILES])
logging.info("Total of source codes/files in the unsafe TEST dataset : %d", informationsFiles[UNSAFE][TOTAL_FILES])
dict_res["testset_files"] = informationsFiles

informationsFiles = retrieve_informations_about_dataset(VALID_SET_PATH)
logging.info("Total of source codes/files in the whole VALIDATION dataset : %d ", informationsFiles[TOTAL_IN_DATASET])
logging.info("Total of source codes/files in the safe VALIDATION dataset : %d", informationsFiles[SAFE][TOTAL_FILES])
logging.info("Total of source codes/files in the unsafe VALIDATION dataset : %d", informationsFiles[UNSAFE][TOTAL_FILES])
dict_res["validset_files"] = informationsFiles

with open(JSON_PATH, 'w') as json_file:
    json.dump(dict_res, json_file, indent=3)

