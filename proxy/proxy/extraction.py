#!/usr/bin/env python
# -*-coding:Utf-8 -*-

'''
Created on Jun 14, 2012

Executable module for information extraction

@author: Gaylord Cherencey
'''

from model import DataBase
import functions
import logging
import os
import re
import tarfile

SUCCESS = 0
FAILURE = 1

def main(args=None):

    #Check the options and arguments parsed

    parser = functions.defineParser()

    (options, args) = parser.parse_args(args)

    if len(args) == 0:
        parser.error("You have to put a file name")

    elif len(args) == 1:
        parser.error("You didn't put any name for the database")

    elif len(args) != 2:
        parser.error("Incorrect number of arguments")

    logging.basicConfig(format = '%(asctime)s -> %(levelname)s : %(message)s',
                        level = options.level,
                        datefmt = '%m/%d/%Y %I:%M:%S %p')

    for arg in args:
        logging.info("Argument passed %s", arg)

    if os.path.exists(args[0]):

        print "Started ..."
        logging.debug('Started')

        tarball = tarfile.open(args[0])

        db = DataBase(args[1])

        #Go throw the tarball and extract the tar file
        # k -> name of the job
        # v dictionary with the data ( { 'connections':[], 'inputs': [], 'site': '' } )
        for k,v in functions.extract(tarball, condition = myCondition_1, extractor = myExtractor_1):

            print "Add data to DB... => ",k ,v

            try:
                db.add_Data(k, v)

            except KeyError:
                logging.warning("Wrong tarfile")

        logging.debug("************************************************************************************")
        print "Extraction done"
        logging.debug('Done')
        return SUCCESS

    else:
        print 'The file does not exist'
        return FAILURE

def myCondition_1(name):
    """Set the conditions for the extraction of the tarfiles"""

    if name.endswith(".tgz"):
        return True

    else:
        return False

def myExtractor_1(tarFile,tarInfo):
    """To define the way we extract the data from a tarfile"""

    logging.debug("***********************************************************************************")

    logging.debug("Find a zip in tarFile: %s", tarInfo.name)
    exFileObject = tarFile.extractfile(tarInfo)
    logging.debug("Extraction...")
    tarFileObject = tarfile.open(fileobj = exFileObject)
    logging.debug("Turning on : %s", tarFileObject.name)

    key = re.split(r"(\d{8}_\d{8})", tarInfo.name)

    return key[1], dict(functions.extract(tarFileObject, extractor = myExtractor_2,  condition = myCondition_2))

    logging.debug("******************** End of the research for this tar file ************************")


def myCondition_2(name):
    """Set the conditions for the extraction of the files"""

    if re.match(name, "job.info"):
        return 1

    if functions.isThisTypeOfFile(name, "xml"):
        return 2

    if functions.isThisTypeOfFile(name, "log"):
        return 3

    else:
        return 0

def myExtractor_2(tarFile,tarInfo):
    """To define the way we extract the data from a file depending of the extension"""

    if myCondition_2(tarInfo.name) is 1:
        site = functions.getSite(tarInfo, tarFile)
        return "site", site

    if myCondition_2(tarInfo.name) is 2:
        inputs = functions.getInputs2(tarInfo, tarFile)
        return "inputs", inputs

    if myCondition_2(tarInfo.name) is 3:
        connections = functions.getConnections(tarInfo, tarFile)
        return "connections", connections

##########################################
# permitted to make the module executable

if __name__ == "__main__":
    main()
