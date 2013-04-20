#!/usr/bin/env python
# -*-coding:Utf-8 -*-

'''
Created on Jul 12, 2012

Executable module for analysis of the data

@author: Gaylord Cherencey
'''

from model import DataBase, Input, Site, Job, Connection
from optparse import OptionParser
import logging
import os
import proxy
import random
import re

SUCCESS = 0
FAILURE = 1

# proxies dictionary contains every proxy object for every site
# ex -> proxy["LCG.RAL.uk"]
proxies = {}

def main(args=None):
    '''Main method which get the list_For_Ratio regarding some parameters (db, seed_Number, ratio_Number, max_Time)
       calculate the global_ratio and then add it to a csv file
    '''
    response = defineParser(args)

    if os.path.exists(response[0]):

        print "Started ..."
        logging.debug('Started')

        db = DataBase(response[0])
        seed_Number = int(response[1])
        ratio_Number = int(response[2])
        max_Time = int(response[3])
        ratio_CSV = response[4]

        #Creation of a proxy for every site (parameter : maxTime)
        list_Site = db.session.query(Site).all()

        proxies["ALL"] = proxy.Proxy(max_Time)

        for site in list_Site:
            proxies[site.name] = proxy.Proxy(max_Time)

        #Get and send every request into the proxy class
        list_Request = getRequest(db, seed_Number, ratio_Number)

        for url, (site, time) in list_Request :
            proxies["ALL"].request(url, time)
            proxies[site].request(url, time)

        #number_site is needed into the CSV files in order to create 3D plots
        number_site = 0

        #Creation of every CSV files
        #eample of hit ratio csv file raw : 70,30,47.504 (ratio, max_time(minutes), hit_ratio(pourcentage))
        #example of requestperhour csv file raw : 6,704,1 (number_site, time(hours), number of data for this bin)
        #example of delta csv file raw : 6,704,1 (number_site, time(minutes), number of data for this bin)
        for site in sorted(proxies):

            if  os.path.exists(site + "_" + response[0] + '_Delta.csv') is False and ratio_Number == 250:
                proxies[site].histograms["Delta"].create_CSV(site + "_" + response[0] + '_Delta.csv', number_site)

            if  os.path.exists(site + "_" + response[0] + '_RequestPerhour.csv') is False and ratio_Number == 250:
                proxies[site].histograms["RequestPerHour"].create_CSV(site + "_" + response[0] + '_RequestPerhour.csv', number_site)

            number_site += 1

            proxies[site].createHitRatioCSV(site + '_' + ratio_CSV, ratio_Number, max_Time)

        print "Analysis done for parameters " + str(response[:5])
        logging.debug("Analysis done for parameters " + str(response[:5]))

    else:
        print 'The file does not exist'

def getRequest(db, seed_Number, ratioNumber):
    '''Method which get all the input coming from the database for injection into the proxy module'''

    list_Input_File = []

    list_Inputs = db.session.query(Input).all()
    list_Site_Connection = db.session.query(Site.name, Connection.time).filter(Input.id_Job == Job.id_Job).\
                                                        filter(Job.id_Job == Connection.id_Job).\
                                                        filter(Job.id_Site == Site.id_Site).all()

    list_URL = range(1, ((len(list_Inputs)/ratioNumber))+1) * (ratioNumber)

    random.seed(seed_Number)
    random.shuffle(list_URL)

    for element in list_Site_Connection:
        if element[1]:
            name_site = element[0]
            result = re.match(r'^(\d{4}-\d{2}-\d{2} *\d{2}:\d{2}:\d{2})', element[1])
            list_Input_File.append((name_site, result.group(1)))

    list_Input_File = sorted(list_Input_File, key = lambda ((site, time)): time)

    return zip(list_URL, list_Input_File)

def defineParser(args):
    """Definition of the parser and the behavior following the options"""

    parser = OptionParser(usage="""Usage: %prog db seed_Number ratio_Number max_Time ratio_CSV [options] : Use the -h option to get help

       db -> the name of your database file
       seed_Number -> certain way to shuffle the input data
       ratio_Number -> parameter to group the inputs
       max_time -> the maximum time you want your object into the proxy cache
       ratio_CSV -> name of the CSV File created """)

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

    (options, args) = parser.parse_args(args)

    if len(args) == 0:
        parser.error("You have to put parameters")

    elif len(args) == 1:
        parser.error("You didn't put any name for the database")

    elif len(args) < 5:
        parser.error("Not enough arguments")

    elif len(args) != 5:
        parser.error("Too much arguments")

    logging.basicConfig(format = '%(asctime)s -> %(levelname)s : %(message)s',
                        level = options.level,
                        datefmt = '%m/%d/%Y %I:%M:%S %p')

    logging.info("Argument passed %s", args)

    #We return the options.level only for the test method
    return args

##########################################
# permitted to make the module executable

if __name__ == '__main__':
    main()