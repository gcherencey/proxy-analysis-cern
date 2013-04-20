'''
Created on Jun 13, 2012

Module with all the funtions usefull for extraction

@author: Gaylord Cherencey
'''

from XML_Extraction import MySaxDocumentHandler
from xml.sax import make_parser
import xml.etree.ElementTree as ET

from optparse import OptionParser
import logging
import re

def defineParser():
    """Definition of the parser and return it"""

    parser = OptionParser(usage="Usage: %prog name_of_the_tarball name_for_database [options] : Use the -h option to get help")

    parser.add_option("-v", "--verbose",
                      action = "store_const",
                      const = logging.INFO,
                      dest = "level",
                      help = "Print a message each time  a  module  is initialized")
    parser.add_option("-d", "--debug",
                      action = "store_const",
                      const = logging.DEBUG,
                      dest = "level",
                      help = "Print debug information")

    return parser

def extract(filename_or_Object, condition=None, extractor=None):
    """Generic method for data extraction from tarfile"""
    #We do and return the file extracted only if the condition is true e.g member is a tar file
    return (extractor(filename_or_Object,tarInfo) for tarInfo in filename_or_Object if condition(tarInfo.name))

def isThisTypeOfFile(name, extension):
    """Determine if the member is a extension file

       name : name of the file we want to check
       extension : condition for the extension check
    """

    pattern = re.compile("Brunel_\d*_\d*_\d." + extension + '$')

    if pattern.search(name):
        return True

    else:
        return False

def getConnections(member, tarFileObject):
    """Extract the ligns in the log files which contains the words : 'Connected to database'"""
    data = []

    dataFile = tarFileObject.extractfile(member)
    logging.debug("Extraction of *.log file...")
    logging.debug("Research in the file %s :", member.name)

        #We extract all the log file and go throw them to find the lines containing 'Requested to process'
        #From those lines we keep the date, the time and the purpose of the connection
        #Ex : 2012-05-19  16:40:58 UTC    BrunelInit
    for line in dataFile:
        result = re.match(r'(\d{4}-\d{2}-\d{2}) *(\d{2}:\d{2}:\d{2} \S*) (\S*) *\S* *Requested to process', line)

        #If the result is not None we return it as a proper string
        if result:
            resultAsString = (r"{0}  {1}    {2}").format(result.group(1), result.group(2), result.group(3))
            data.append(resultAsString)

    logging.debug("Give back data : %s", data)
    return data

def getInputs(member, tarFileObject):
    """Extract the inputs from the XML file using xml.tree

        This method take to much execution time so we will use getInputs2 which use xml.sax
    """

    logging.debug("Find a XML file : %s", member.name)

    inputFile = tarFileObject.extractfile(member)

    tree = ET.parse(inputFile)
    elems = tree.findall("input/file")

    for elem in elems:
        logging.debug("Find a input : %s", elem.attrib["name"])
        return elem.attrib["name"]

def getInputs2(member, tarFileObject):
    """Extract the inputs from the XML file using xml.sax"""

    logging.debug("Find a XML file : %s", member.name)

    handler = MySaxDocumentHandler()

    parser = make_parser()

    parser.setContentHandler(handler)
    inputFile = tarFileObject.extractfile(member)

    parser.parse(inputFile)
    inputFile.close()

    inputs = handler.get_inputsList()

    logging.debug("Find a input : %s", inputs)

    return inputs

def getSite(member, tarFileObject):
    """Extract the site from the .info file"""

    logging.debug("Find a info file : %s", member.name)
    dataFile = tarFileObject.extractfile(member)
    for line in dataFile:

        result = re.match(r'/Site = (\S*)', line)

        if result:
            site = result.group(1)
            logging.debug("Find the location : %s", site)
            return site