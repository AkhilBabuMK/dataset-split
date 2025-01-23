import os
import logging
from pathlib import Path
from os import walk

def create_folder_if_not_exist(path) :

    if not os.path.exists(path) :
        os.makedirs(path, exist_ok=True)
        logging.debug("%s doesn't exist ==> creation of this folder",path)
    else :
         logging.debug("%s exist ==> do nothing",path)

def get_list_dir_recursively(path, format=None):
    listeFichiers = []
    for (repertoire, sousRepertoires, fichiers) in walk(path):
        print(f"{repertoire} {sousRepertoires} {fichiers}")
        if fichiers :
            if format == "str" :
                fichiers_with_root = [Path(repertoire, f).__str__() for f in fichiers ]
            else :
                fichiers_with_root = [Path(repertoire, f) for f in fichiers ]
            listeFichiers.extend(fichiers_with_root)
    return listeFichiers