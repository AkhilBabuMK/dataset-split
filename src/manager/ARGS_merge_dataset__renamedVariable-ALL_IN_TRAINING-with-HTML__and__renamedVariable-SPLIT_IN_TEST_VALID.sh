#!/bin/sh
######## EXAMPLE TO CALL THE SCRIPT
####  ./ARGS_merge_dataset__renamedVariable-ALL_IN_TRAINING-with-HTML__and__renamedVariable-SPLIT_IN_TEST_VALID.sh
# ARG 1 /absolute/path/db/HOP-renamedVariable-data-TRAIN-template-with-HTML-D1
# ARG 2 /absolute/path/db/HOP-renamedVariable-data-SPLIT_IN_TEST_VALID-with-HTML-D1
# ARG 3 HOP-final-preprocessed-data-v6-renamedVariable-with-r3-r4_11-template-ALL_IN_TRAINING__renamedVariable-with-r0-r1-r2-r5_14-template_SPLIT_IN_TEST_VALID-with-HTML-D1

SOURCE=$1
echo $SOURCE;

SOURCE_TRAIN_SAFE=$SOURCE/"trainset_files/safe/"
SOURCE_TRAIN_UNSAFE=$SOURCE/"trainset_files/unsafe/"
SOURCE_TEST_SAFE=$SOURCE"/testset_files/safe/"
SOURCE_TEST_UNSAFE=$SOURCE"/testset_files/unsafe/"
SOURCE_VALID_SAFE=$SOURCE"/validset_files/safe/"
SOURCE_VALID_UNSAFE=$SOURCE"/validset_files/unsafe/"



SOURCE2=$2
echo $SOURCE2;
SOURCE2_TRAIN_SAFE=$SOURCE2"/trainset_files/safe/"
SOURCE2_TRAIN_UNSAFE=$SOURCE2"/trainset_files/unsafe/"
SOURCE2_TEST_SAFE=$SOURCE2"/testset_files/safe/"
SOURCE2_TEST_UNSAFE=$SOURCE2"/testset_files/unsafe/"
SOURCE2_VALID_SAFE=$SOURCE2"/validset_files/safe/"
SOURCE2_VALID_UNSAFE=$SOURCE2"/validset_files/unsafe/"

###### NE PAS OUBLIER DE CHANGER CE CHEMIN SI ON CHANGE DE VERSIONDE DB
DES="/absolute/path/db/"
DES_RESULT=$DES/$3
echo $DES_RESULT;

DES_TRAIN_SAFE=$DES_RESULT/"trainset_files/safe/"
DES_TRAIN_UNSAFE=$DES_RESULT/"trainset_files/unsafe/"
DES_TEST_SAFE=$DES_RESULT/"testset_files/safe/"
DES_TEST_UNSAFE=$DES_RESULT/"testset_files/unsafe/"
DES_VALID_SAFE=$DES_RESULT/"validset_files/safe/"
DES_VALID_UNSAFE=$DES_RESULT/"validset_files/unsafe/"



echo "BEGIN SCRIPT";
echo $SOURCE;
echo $SOURCE_TRAIN_SAFE;
echo $SOURCE_TEST_SAFE;
echo $SOURCE_VALID_SAFE;
echo $SOURCE2;
echo $SOURCE2_TRAIN_SAFE;
echo $SOURCE2_TEST_SAFE;
echo $SOURCE2_VALID_SAFE;
echo "DEST FOLDER";
echo $DES_RESULT;
echo $DES_TRAIN_SAFE;
echo $DES_TEST_SAFE;
echo $DES_VALID_SAFE;



mkdir -p $DES_TRAIN_SAFE & mkdir -p $DES_TRAIN_UNSAFE & mkdir -p $DES_TEST_SAFE & mkdir -p $DES_TEST_UNSAFE & mkdir -p $DES_VALID_SAFE & mkdir -p $DES_VALID_UNSAFE;
rsync -a $SOURCE_TRAIN_SAFE $DES_TRAIN_SAFE & rsync -a $SOURCE_TRAIN_UNSAFE $DES_TRAIN_UNSAFE & rsync -a $SOURCE_TEST_SAFE $DES_TEST_SAFE & rsync -a $SOURCE_TEST_UNSAFE $DES_TEST_UNSAFE & rsync -a $SOURCE_VALID_SAFE $DES_VALID_SAFE & rsync -a $SOURCE_VALID_UNSAFE $DES_VALID_UNSAFE &
rsync -a $SOURCE2_TRAIN_SAFE $DES_TRAIN_SAFE & rsync -a $SOURCE2_TRAIN_UNSAFE $DES_TRAIN_UNSAFE & rsync -a $SOURCE2_TEST_SAFE $DES_TEST_SAFE & rsync -a $SOURCE2_TEST_UNSAFE $DES_TEST_UNSAFE & rsync -a $SOURCE2_VALID_SAFE $DES_VALID_SAFE & rsync -a $SOURCE2_VALID_UNSAFE $DES_VALID_UNSAFE


