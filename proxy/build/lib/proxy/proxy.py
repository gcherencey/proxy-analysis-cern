'''
Created on Jul 10, 2012

Proxy simulation

@author: Gaylord Cherencey
'''

import bisect
import csv
import datetime

class Proxy:
    '''Class which simulate a proxy area with a simple policy :
            If the object it's in the cache since more than maxTime we refresh the object by asking the server
    '''

    def __init__(self, maxTime):
        '''Method which initialize the proxy
            - self.cache contains url:time
            - self.histogramm contains every Histogram object
            - self.max represent the time that a object can stay in the cache
            - self.hit you add +1 if the object is in the cache
            - self.miss you add +1 if the object is not in the cache
            - self.formatTime permit to precise how to transform a string into a datetime object
            - self.timeref is the reference date to calculate delta
        '''

        self.cache = {}
        self.histograms = {}

        #Creation of the two histogram: Delta and RequestPerHour
        self.histograms["Delta"] = Histogram(0 , 200 , 40)
        self.histograms["RequestPerHour"] = Histogram(190740, 190840 , 100)

        self.max = datetime.timedelta(minutes = maxTime)
        self.min = datetime.timedelta(hours = 0)
        self.hit = 0.00
        self.miss = 0.00
        self.formatTime = '%Y-%m-%d  %H:%M:%S'
        self.timeref = datetime.datetime.strptime("1990-08-07 00:00:00", self.formatTime)


    def request(self, url, time):
        '''Method which simulate a request to the proxy to get a object :
            the proxy check it the object (url) is already in the cache or not regarding the time
        '''

        formatedTime = datetime.datetime.strptime(time, self.formatTime)

        self.fillRequestPerHourHisto(formatedTime - self.timeref)

        #if the object is already in the cache
        if url in self.cache:

            cache_time = self.cache[url]

            #if the time between this request and the previous one is under self.max we increment self.hit
            if formatedTime - cache_time < self.max:
                self.cache[url] = cache_time
                self.hit += 1

            #otherwise we increment self.miss and add the delta time at the delta histogram
            else:
                self.miss += 1
                self.cache[url] = formatedTime

                self.fillDeltaHisto(formatedTime - cache_time)

        #we add the url if it not in the cache
        else :
            self.cache[url] = formatedTime
            self.miss += 1

    def hitRatio(self):
        '''Method which calculate the hit cache ratio : hitRatio = self.hit / (self.hit + self.miss)'''

        hitRatio = self.hit / (self.hit + self.miss)

        return round(hitRatio * 100, 3)

    def createHitRatioCSV(self, name_CSV, ratio_Number, max_Time):
        '''Method which create the hit ratio CSV file

            name_CSV will be the name of the CSV file
            ratio_number is the ratio use to calculate this hit ratio
            max_Time is the max_time coming from the proxy used to calculate the cache hit ratio
        '''

        list_Ratio_CSV = []

        list_Ratio_CSV.append(ratio_Number)
        list_Ratio_CSV.append(max_Time)

        #We open the file in ab mode to add every hit ratio regarding the max_time and ratio
        ratio_file_CSV = csv.writer(open(name_CSV, "ab"))

        list_Ratio_CSV.append(self.hitRatio())

        ratio_file_CSV.writerow(list_Ratio_CSV)

    def fillDeltaHisto(self,delta):
        '''Method which add the delta to the delta histogram and transform it into seconds'''

        if delta :
            deltagroup = (delta.seconds + (delta.days *86400))/60
            self.histograms["Delta"].addData(deltagroup)

    def fillRequestPerHourHisto(self, data):
        '''Method which add the data to the requestperhour histogram and transform it into hours'''

        if data :
            dataHour = (data.seconds + (data.days * 86400))/3600
            self.histograms["RequestPerHour"].addData(dataHour)

class Histogram:
    '''Histogram class which permit to get the data bin and create CSV file

       - self.max the maximun number for the histogram
       - self.min the minimum number for the histogram
       - self.number_bins use to know how many bins will have the histogram
       - self.all_data dictionary which contains all the data ( { bin : number of data for this bin } )
    '''

    def __init__(self, min , max, number_bins):

        self.max = max
        self.min = min
        self.number_bins = number_bins
        self.all_data = {}

    def addData(self, data):
        bin = int( (data - self. min) * self.number_bins / (self.max - self.min) )
        self.all_data[bin] = self.all_data.get((bin), 0) + 1

    def create_CSV(self, name, site):

        histo_CSV = csv.writer(open(name, "w"))
        keys = self.all_data.keys()

        for i in range(min(keys), max(keys), ((self.max - self.min)/self.number_bins)):
            histo_CSV.writerow([site, i, self.all_data.get((i), 0)])
