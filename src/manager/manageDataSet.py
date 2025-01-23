import logging
import os
import random
from math import ceil, floor

import numpy as np

from src.manager.manageFolder import create_folder_if_not_exist

SAFE = "safe"
UNSAFE = "unsafe"
TOTAL_IN_DATASET = "total"
FILES = "files"
PATH = 'path'
TOTAL_FILES = 'totalFiles'
SAVE_NUMPY_XSS_DATASET_PATH_BY_DEFAULT = "/absolute/path/data/numpy_dataset/XSS_dataset/"
TRAIN_X_DATA_NUMPY_FILE_NAME = 'X_train_XSS.npy'
TRAIN_Y_DATA_NUMPY_FILE_NAME = 'Y_train_XSS.npy'
TEST_X_DATA_NUMPY_FILE_NAME = 'X_test_XSS.npy'
TEST_Y_DATA_NUMPY_FILE_NAME = 'Y_test_XSS.npy'
TRAIN_X_DATA_NUMPY_FILE_NAME_COMPRESSED = 'X_train_XSS.npz'
TRAIN_Y_DATA_NUMPY_FILE_NAME_COMPRESSED = 'Y_train_XSS.npz'
TEST_X_DATA_NUMPY_FILE_NAME_COMPRESSED = 'X_test_XSS.npz'
TEST_Y_DATA_NUMPY_FILE_NAME_COMPRESSED = 'Y_test_XSS.npz'

def getNumberOfDataInEachSet(total, withval=False) :
    """

    :param total: number of file in the whole dataset
    :return: tuple - (number of data in the train set, number of data in the test set)
    """
    if withval :
        trainSet, testSet, validSet = round(total * 80 / 100), round(total * 10 / 100), round(total * 10 / 100)
        trainSet, testSet, validSet = ceil(total * 80 / 100), round(total * 10 / 100), round(total * 10 / 100)
        trainSet, testSet, validSet = floor(total * 80 / 100), round(total * 10 / 100), round(total * 10 / 100)
        #trainSet, testSet, validSet = round(total * 80 / 100), floor(total * 10 / 100), round(total * 10 / 100)
        return trainSet, testSet, validSet
    trainSet, testSet = round(total * 70/100), round(total * 30/100)
    return trainSet, testSet

def getNumberOfDataInEachSetCustom(total, purcentage_train, purcentage_test, purcentage_valid, withval=False) :
    """

    :param total: number of file in the whole dataset
    :return: tuple - (number of data in the train set, number of data in the test set)
    """
    if withval :
        trainSet, testSet, validSet = round(total * purcentage_train), round(total * purcentage_test), round(total * purcentage_valid)
        #trainSet, testSet, validSet = ceil(total * purcentage_train), round(total * purcentage_test), round(total * purcentage_valid)
        #trainSet, testSet, validSet = floor(total * purcentage_train), round(total * purcentage_test), round(total * purcentage_valid)
        #trainSet, testSet, validSet = round(total * purcentage_train), floor(total * purcentage_test), round(total * purcentage_valid)
        #trainSet, testSet, validSet = round(total * purcentage_train), ceil(total * purcentage_test), round(total * purcentage_valid)
        return trainSet, testSet, validSet
    trainSet, testSet = round(total * 70/100), round(total * 30/100)
    return trainSet, testSet

def getNumberOfDataInEachSet69pc1pc30pc(total, withval=False) :
    """

    :param total: number of file in the whole dataset
    :return: tuple - (number of data in the train set, number of data in the test set)
    """
    if withval :
        trainSet, testSet, validSet = round(total * 69 / 100), round(total * 1 / 100), round(total * 30 / 100)
        return trainSet, testSet, validSet
    trainSet, testSet = round(total * 70/100), round(total * 30/100)
    return trainSet, testSet




def retrieve_informations_about_dataset(path) :
    """
    @return : dictionnary such as :
    - key : absolute path of each folder contains in the folder path
    - el : dictionnary such as :
        - key : totalFiles
        - el : number of files in the folder corresponding to the key names
    """
    informationsFiles = {TOTAL_IN_DATASET : 0}
    for root, name, files in os.walk(path):
        lenFiles = len(files)
        informationsFiles = setInformationsFiles(informationsFiles, root, lenFiles, files )
        informationsFiles = setTotalInDataset(informationsFiles, lenFiles)
    return informationsFiles


def setInformationsFiles(informationsFiles, root, lenFiles, files ) :
    """

    :param informationsFiles: dictionary to informations about the dataset
    :param root: root path of the folder
    :param lenFiles: number of files in the current folder
    :param files: list of files inside the current folder
    :return:
    """
    tmp = root.split('/')
    if SAFE in tmp:
        informationsFiles[SAFE] = {'totalFiles': lenFiles, 'safe?': 1, 'path': root, FILES : files}
    elif UNSAFE in tmp:
        informationsFiles[UNSAFE] = {'totalFiles': lenFiles, 'safe?': 0, 'path': root, FILES : files}
    return informationsFiles


def setTotalInDataset(informationsFiles, lenFiles) :
    """

    :param informationsFiles: dictionary of informations about the dataset
    :param lenFiles: number of files in the current folder
    :return: dictionary of informations modified with the total of files in the whole dataset
    """
    informationsFiles[TOTAL_IN_DATASET] = informationsFiles[TOTAL_IN_DATASET] + lenFiles
    return informationsFiles


def shuffleDataSet(X_safe, Y_safe, X_unsafe, Y_unsafe) :
    X_list = X_safe + X_unsafe
    Y_list = Y_safe + Y_unsafe
    mapIndexPosition = list(zip(X_list, Y_list))
    random.shuffle(mapIndexPosition)
    X_list, Y_list = zip(*mapIndexPosition)
    return X_list, Y_list


def divideDataSet(totalInTrainSet, shuffle_list, withvaliditation=False, totalInValidationSet=0) :
    if withvaliditation and totalInValidationSet != 0 :
        logging.debug("VALIDATION HERE %d", totalInValidationSet)
        logging.info("training  --> %d", len(shuffle_list[: totalInTrainSet]))
        logging.info("testing -->  %d", len(shuffle_list[totalInTrainSet:totalInTrainSet+ totalInValidationSet]))
        logging.info("valid --> %d", len(shuffle_list[totalInTrainSet+ totalInValidationSet:]))
        trainAndValid = totalInTrainSet+ totalInValidationSet
        return shuffle_list[: totalInTrainSet], shuffle_list[totalInTrainSet:trainAndValid], shuffle_list[trainAndValid:]
    return shuffle_list[: totalInTrainSet], shuffle_list[totalInTrainSet:], []

def divide_database_in_3_sets(shuffle_list, total_train_set, total_test_set, total_validation_set) :
    logging.info("total_train_set  --> %d", total_train_set)
    logging.info("total_test_set -->  %d", total_test_set)
    logging.info("total_validation_set --> %d", total_validation_set)
    logging.info("shuffle_list --> %d", len(shuffle_list))
    logging.info("shuffle_list --> %s", shuffle_list[: total_train_set])
    train_set = shuffle_list[: total_train_set]
    test_set =  shuffle_list[total_train_set:total_train_set+total_test_set]
    # test_set =  shuffle_list[total_train_set:]
    valid_set =  shuffle_list[total_train_set+total_test_set: total_train_set+total_test_set+total_validation_set]
    logging.info("training  --> %d", len(train_set))
    logging.info("testing -->  %d", len(test_set))
    logging.info("testing -->  %s", shuffle_list[total_train_set:total_test_set])
    logging.info("valid --> %d", len(valid_set))
    return train_set, test_set, valid_set


def getXYSafeAndUnSafeSets(informationsFiles) :
    return [os.path.join(informationsFiles[SAFE][PATH],file) for file in informationsFiles[SAFE][FILES]], getYSet(informationsFiles[SAFE][TOTAL_FILES], SAFE) ,\
           [os.path.join(informationsFiles[UNSAFE][PATH],file) for file in informationsFiles[UNSAFE][FILES]], getYSet(informationsFiles[UNSAFE][TOTAL_FILES], UNSAFE)


def getYSet(total, safe) :
    return  [1] * total if (safe==SAFE) else [0] * total


def saveNumpyDataset(X_train, Y_train, X_test, Y_test, folder_path=SAVE_NUMPY_XSS_DATASET_PATH_BY_DEFAULT) :
    create_folder_if_not_exist(folder_path)
    path = os.path.join(folder_path, TRAIN_X_DATA_NUMPY_FILE_NAME)
    np.save(path, X_train)
    logging.info("Saving X_train set in numpy file --> %s ", path)
    path = os.path.join(folder_path, TRAIN_X_DATA_NUMPY_FILE_NAME_COMPRESSED)
    np.savez_compressed(path, X_train)
    logging.info("Saving X_train set in compressed numpy file --> %s " + path)

    path = os.path.join(folder_path, TRAIN_Y_DATA_NUMPY_FILE_NAME)
    np.save(path, Y_train)
    logging.info("Saving Y_train set in numpy file --> %s ", path)
    path = os.path.join(folder_path, TRAIN_Y_DATA_NUMPY_FILE_NAME_COMPRESSED)
    np.savez_compressed(path, Y_train)
    logging.info("Saving train set in compressed numpy file --> %s " + path)

    path = os.path.join(folder_path, TEST_X_DATA_NUMPY_FILE_NAME)
    np.save(path, X_test)
    logging.info("Saving X_test set in numpy file --> %s ", path)
    path = os.path.join(folder_path, TEST_X_DATA_NUMPY_FILE_NAME_COMPRESSED)
    np.savez_compressed(path, X_test)
    logging.info("Saving X_test set in compressed numpy file --> %s " , path)

    path = os.path.join(folder_path, TEST_Y_DATA_NUMPY_FILE_NAME)
    np.save(path, Y_test)
    logging.info("Saving Y_test set in numpy file --> %s " + path)
    path = os.path.join(folder_path, TEST_Y_DATA_NUMPY_FILE_NAME_COMPRESSED)
    np.savez_compressed(path, Y_test)
    logging.info("Saving Y_test set in compressed numpy file --> %s " , path)

def retrieveNumpyDataset(folder_path=SAVE_NUMPY_XSS_DATASET_PATH_BY_DEFAULT) :
    try :

        path = os.path.join(folder_path, TRAIN_X_DATA_NUMPY_FILE_NAME)
        X_train = np.load(path)

        path = os.path.join(folder_path, TRAIN_Y_DATA_NUMPY_FILE_NAME)
        Y_train = np.load(path)

        path = os.path.join(folder_path, TEST_X_DATA_NUMPY_FILE_NAME)
        X_test = np.load(path)

        path = os.path.join(folder_path, TEST_Y_DATA_NUMPY_FILE_NAME)
        Y_test = np.load(path)
        return X_train, Y_train, X_test, Y_test
    except FileExistsError :
        saveNumpyDataset(X_train, Y_train, X_test, Y_test)


