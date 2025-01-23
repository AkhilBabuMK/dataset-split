import json
import logging
import os
from shutil import copy
from threading import Thread

from src.manager.manageDataSet import retrieve_informations_about_dataset, SAFE, PATH, UNSAFE, TOTAL_IN_DATASET, \
    getNumberOfDataInEachSetCustom, TOTAL_FILES, getYSet, shuffleDataSet, FILES
from src.manager.manageFolder import create_folder_if_not_exist


class CreateCode2VecSets(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, Y_list, X_list, new_safe_path, new_unsafe_path, dataset=None, informationsFiles=None, JS=False):
        Thread.__init__(self)
        self.informationsFiles = informationsFiles if informationsFiles else retrieve_informations_about_dataset(dataset)
        self.Y_list = Y_list
        self.X_list = X_list
        self.new_safe_path = new_safe_path
        self.new_unsafe_path = new_unsafe_path
        self.JS = JS

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        Y_len = len(self.Y_list)
        logging.info("number of file in Y trainset shuffled %d", Y_len)
        for i in range(0,Y_len) :
            if self.Y_list[i] :
                source_path = os.path.join(self.informationsFiles[SAFE][PATH], self.X_list[i])
                copy(source_path, self.new_safe_path)


            else :
                source_path = os.path.join(self.informationsFiles[UNSAFE][PATH], self.X_list[i])
                copy(source_path, self.new_unsafe_path)
            if(i == Y_len-1 ) : logging.info("END OF FOR number of file in Y trainset shuffled %d", i+1)
        if self.JS :
            os.system("find " + os.path.join(self.informationsFiles[UNSAFE][PATH]) + " -name '*.php' -exec sh -c " + '\'mv "$0" "${0%.php}.js"\' {} \;')
            os.system("find " + os.path.join(
                self.informationsFiles[SAFE][PATH]) + " -name '*.php' -exec sh -c " + '\'mv "$0" "${0%.php}.js"\' {} \;')


def create_datasets_from(dataset, purcentage_train, purcentage_test, purcentage_valid,
                         func_to_divide_database_in_datasets, json_config_path,
                         train_set_path, test_set_path, valid_set_path, json_path):
    create_folder_if_not_exist(json_config_path)
    informationsFiles = retrieve_informations_about_dataset(dataset)
    total_in_dataset = informationsFiles[TOTAL_IN_DATASET]
    logging.info("Total of source codes/files in the whole dataset : %d ", total_in_dataset)
    total_trainset, total_testset, total_validset = getNumberOfDataInEachSetCustom(total_in_dataset, purcentage_train,
                                                                                   purcentage_test,
                                                                                   purcentage_valid, withval=True)
    logging.info("In the end, Total of source codes/files in the train dataset has to be %s pc: %d", purcentage_train, total_trainset)
    logging.info("In the end, Total of source codes/files in the test dataset has to be %s pc: %d", purcentage_test,
                 total_testset)
    logging.info("In the end, Total of source codes/files in the valid dataset has to be %s pc: %d", purcentage_valid,
                 total_validset)

    total_safe_files = informationsFiles[SAFE][TOTAL_FILES]
    logging.info("Total of source codes/files in the safe dataset : %d", total_safe_files)
    total_unsafe_files = informationsFiles[UNSAFE][TOTAL_FILES]
    logging.info("Total of source codes/files in the unsafe dataset : %d", total_unsafe_files)
    assert total_safe_files + total_unsafe_files == total_in_dataset
    Y_SAFE = getYSet(total_safe_files, SAFE)
    logging.info("len Y SAFE : %d", len(Y_SAFE))
    assert total_safe_files == len(Y_SAFE)
    Y_UNSAFE = getYSet(total_unsafe_files, UNSAFE)
    logging.info("len Y UNSAFE : %d", len(Y_UNSAFE))
    assert total_unsafe_files == len(Y_UNSAFE)
    X_list, Y_list = shuffleDataSet(informationsFiles[SAFE][FILES], Y_SAFE, informationsFiles[UNSAFE][FILES], Y_UNSAFE)
    logging.info("number of file in X list shuffled %d", len(X_list))
    logging.info("number of file in Y list shuffled %d", len(Y_list))
    assert total_in_dataset == len(X_list)
    assert total_in_dataset == len(Y_list)
    assert len(X_list) == len(Y_list)
    # Divide X shuffled list in 2 : trainX and TestX
    # X_list_train, X_list_valid, X_list_test = divideDataSet(total_trainset, X_list, withvaliditation=True, totalInValidationSet=total_validset)
    X_list_train, X_list_valid, X_list_test = func_to_divide_database_in_datasets(X_list, total_trainset, total_testset,
                                                   total_validset)
    logging.info("number of file in X trainset shuffled %d == total in the end %d", len(X_list_train), total_trainset)
    logging.info("number of file in X testset shuffled %d == total in the end %d", len(X_list_test), total_testset)
    logging.info("number of file in X validset shuffled %d == total in the end %d", len(X_list_valid), total_validset)
    assert len(X_list_train) == total_trainset
    assert len(X_list_valid) == total_validset
    assert len(X_list_test) == total_testset
    # Y_list_train, Y_list_valid, Y_list_test = divideDataSet(total_trainset, Y_list, withvaliditation=True, totalInValidationSet=total_validset)
    Y_list_train, Y_list_valid, Y_list_test = func_to_divide_database_in_datasets(Y_list, total_trainset, total_testset,
                                                   total_validset)
    logging.info("number of file in Y trainset shuffled %d", len(Y_list_train))
    logging.info("number of file in Y testset shuffled %d", len(Y_list_test))
    logging.info("number of file in X validset shuffled %d == total in the end %d", len(Y_list_valid), total_validset)
    assert len(Y_list_train) == total_trainset
    assert len(Y_list_test) == total_testset
    assert len(Y_list_valid) == total_validset
    assert len(Y_list_train) != len(Y_list_test)
    logging.info("NUMBER OF SAFE IN TRAIN SET %s", Y_list_train.count(1))
    logging.info("NUMBER OF SAFE IN TEST SET %s", Y_list_test.count(1))
    logging.info("NUMBER OF SAFE IN VALID SET %s", Y_list_valid.count(1))
    logging.info("NUMBER OF UNSAFE IN TRAIN SET %s", Y_list_train.count(purcentage_train))
    logging.info("NUMBER OF UNSAFE IN TEST SET %s", Y_list_test.count(purcentage_train))
    logging.info("NUMBER OF UNSAFE IN VALID SET %s", Y_list_valid.count(purcentage_train))
    # THIS ASSERTION CAN NOT BE TRUE ANYMORE because WE DON'T TAKE THE WHOLE DATABASE
    # assert Y_list_train.count(0) + Y_list_test.count(0) +  Y_list_valid.count(0) == total_unsafe_files
    # assert Y_list_train.count(1) + Y_list_test.count(1) + Y_list_valid.count(1)== total_safe_files
    TRAIN_SET_SAFE_PATH = os.path.join(train_set_path, 'safe')
    create_folder_if_not_exist(TRAIN_SET_SAFE_PATH)
    TRAIN_SET_UNSAFE_PATH = os.path.join(train_set_path, 'unsafe')
    create_folder_if_not_exist(TRAIN_SET_UNSAFE_PATH)
    TEST_SET_SAFE_PATH = os.path.join(test_set_path, 'safe')
    create_folder_if_not_exist(TEST_SET_SAFE_PATH)
    TEST_SET_UNSAFE_PATH = os.path.join(test_set_path, 'unsafe')
    create_folder_if_not_exist(TEST_SET_UNSAFE_PATH)
    VALID_SET_SAFE_PATH = os.path.join(valid_set_path, 'safe')
    create_folder_if_not_exist(VALID_SET_SAFE_PATH)
    VALID_SET_UNSAFE_PATH = os.path.join(valid_set_path, 'unsafe')
    create_folder_if_not_exist(VALID_SET_UNSAFE_PATH)
    logging.info("Création des threads")
    # Création des threads
    thread_1 = CreateCode2VecSets(Y_list_train, X_list_train, TRAIN_SET_SAFE_PATH, TRAIN_SET_UNSAFE_PATH,
                                  dataset=dataset)
    thread_2 = CreateCode2VecSets(Y_list_test, X_list_test, TEST_SET_SAFE_PATH, TEST_SET_UNSAFE_PATH, dataset=dataset)
    thread_3 = CreateCode2VecSets(Y_list_valid, X_list_valid, VALID_SET_SAFE_PATH, VALID_SET_UNSAFE_PATH,
                                  dataset=dataset)
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
    informationsFiles = retrieve_informations_about_dataset(train_set_path)
    logging.info("Total of source codes/files in the whole TRAIN dataset : %d ", informationsFiles[TOTAL_IN_DATASET])
    logging.info("Total of source codes/files in the safe TRAIN dataset : %d", informationsFiles[SAFE][TOTAL_FILES])
    logging.info("Total of source codes/files in the unsafe TRAIN dataset : %d", informationsFiles[UNSAFE][TOTAL_FILES])
    dict_res["trainset_files"] = informationsFiles
    informationsFiles = retrieve_informations_about_dataset(test_set_path)
    logging.info("Total of source codes/files in the whole TEST dataset : %d ", informationsFiles[TOTAL_IN_DATASET])
    logging.info("Total of source codes/files in the safe TEST dataset : %d", informationsFiles[SAFE][TOTAL_FILES])
    logging.info("Total of source codes/files in the unsafe TEST dataset : %d", informationsFiles[UNSAFE][TOTAL_FILES])
    dict_res["testset_files"] = informationsFiles
    informationsFiles = retrieve_informations_about_dataset(valid_set_path)
    logging.info("Total of source codes/files in the whole VALIDATION dataset : %d ",
                 informationsFiles[TOTAL_IN_DATASET])
    logging.info("Total of source codes/files in the safe VALIDATION dataset : %d",
                 informationsFiles[SAFE][TOTAL_FILES])
    logging.info("Total of source codes/files in the unsafe VALIDATION dataset : %d",
                 informationsFiles[UNSAFE][TOTAL_FILES])
    dict_res["validset_files"] = informationsFiles
    with open(json_path, 'w') as json_file:
        json.dump(dict_res, json_file, indent=3)