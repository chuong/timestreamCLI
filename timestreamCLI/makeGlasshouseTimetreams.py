# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 14:25:45 2014

@author: chuong nguyen
"""
import sys, os, glob, shutil
import logging

def separateTimeStamp(FileNameList, OnePerDay, TimeStampLength = 22):
    NamePrefixList = []
    TimeStampStrList = []
    ExtensionList = []
    DayStampStrPrev = ""
    NamePrefixPrev = ""
    for FileName in sorted(FileNameList):
        FileName2 = os.path.basename(FileName)
        Extension = os.path.splitext(FileName2)[1]
        NamePrefix = FileName2[:-(TimeStampLength+len(Extension))]
        if NamePrefix[-1] == '_':
            NamePrefix = NamePrefix[:-1]
        TimeStampStr = FileName2[-(TimeStampLength+len(Extension)):-(len(Extension))]
        if OnePerDay and NamePrefix == NamePrefixPrev \
            and DayStampStrPrev in TimeStampStr:
            # for now skip image captured on the same day
            logging.info("Skip image {}".format(FileName))
            continue
        NamePrefixList.append(NamePrefix)
        TimeStampStrList.append(TimeStampStr)
        ExtensionList.append(Extension)
        NamePrefixPrev = NamePrefix[:]
        DayStampStrPrev = TimeStampStr[:10]

    return NamePrefixList, TimeStampStrList, ExtensionList

def createTimeStreamPaths(RootPath, PathList, createNew = True):
    FullPathList = []
    for path in PathList:
        FullPath = os.path.join(RootPath, path)
        FullPathList.append(FullPath)
    return FullPathList

def saveToTimeStream(FileNameList, NamePrefixList, TimeStampList, RootPath):
    for FileName, NamePrefix, TimeStampStr in zip(FileNameList, NamePrefixList,
                                                  TimeStampStrList):
        # create timestream folder
        TSPath    = os.path.join(RootPath, NamePrefix)
        YearPath  = os.path.join(TSPath, TimeStampStr[:4])
        MonthPath = os.path.join(YearPath, TimeStampStr[:7])
        DayPath   = os.path.join(MonthPath, TimeStampStr[:10])
        HourPath  = os.path.join(DayPath, TimeStampStr[11:13])
        if not os.path.exists(HourPath):
            os.makedirs(HourPath)

        # copy the file over if doesn't exist
        NewFile = os.path.join(HourPath, os.path.basename(FileName))
        if not os.path.exists(NewFile):
            print('Copy {} \nto {}'.format(FileName, HourPath))
            shutil.copyfile(FileName, NewFile)
        else:
            print('File {} exists.'.format(NewFile))

if len(sys.argv) < 4:
    RawPath = '/home/chuong/Data/phenocam/a_data/TimeStreams/Borevitz/BVZ0038/_data/BVZ0038-PhenotypeData'
#    RootPath = '/home/chuong/Data/phenocam/a_data/TimeStreams/Borevitz/BVZ0038/_data/BVZ0038-PlantTS'
    RootPath = '/home/chuong/Data/BVZ0038/BVZ0038-PlantTS'
    OnePerDay = True
else:
    RawPath = sys.argv[1]
    RootPath = sys.argv[2]
    OnePerDay = eval(sys.argv[3])

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
day_interval = 2
starDate = [2014, 8, 5] # [year, month, day]
TimeStreamPathSet = ()
for i in range(0, 30, day_interval):
    path = str(starDate[0]) + '_' + str(starDate[1]) + '_' + str(starDate[2]+i)
    path = os.path.join(RawPath, path)
    if os.path.exists(path):
        logging.info('Process ' + path)
        # Process SIDE images
        FileNameList = glob.glob(os.path.join(path, '*SIDE*.jpg'))
        NamePrefixList, TimeStampStrList, ExtensionList = separateTimeStamp(FileNameList, OnePerDay, TimeStampLength = 22)
        saveToTimeStream(FileNameList, NamePrefixList, TimeStampStrList, RootPath)
        FileNameList = glob.glob(os.path.join(path, '*TOP*.jpg'))
        NamePrefixList, TimeStampStrList, ExtensionList = separateTimeStamp(FileNameList, OnePerDay, TimeStampLength = 22)
        saveToTimeStream(FileNameList, NamePrefixList, TimeStampStrList, RootPath)