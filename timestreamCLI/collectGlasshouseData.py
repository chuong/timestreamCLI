# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 11:47:46 2014

@author: chuong
"""
from __future__ import print_function
import sys
import glob
import os
import csv
import datetime
import time
import numpy as np
import matplotlib.pylab as plt

if len(sys.argv) == 1:
    RootPath = "/home/chuong/Data/BVZ0038/BVZ0038-ProcessedPlantTSP-results_old/"
else:
    RootPath = sys.argv[1]

Views = ["SIDE", "TOP"]
Features = ["area", "compactness", "eccentricity", "perimeter", "roundness",
            "height", "wilting", "height2", "wilting2"]
FoldersViews = [glob.glob(os.path.join(RootPath, "*" + View)) for View in Views]
FoldersViews = [sorted(FoldersView) for FoldersView in FoldersViews]
# remove folder of background images
FoldersViews = [FoldersViews[0][:-1], FoldersViews[1][:-1]]

for Feature in Features:
    for j in range(len(Views)):
        TimeStamptsAll = []
        FeatureListAll = []
        for Folder in FoldersViews[j]:
            FeatureCSV = os.path.join(Folder, "csv", "{}.csv".format(Feature))
            print("Read {}".format(FeatureCSV))
            with open(FeatureCSV, "r") as csvfile:
                TimeStampts = []
                FeatureList = []
                csvreader = csv.reader(csvfile, delimiter=',')
                for i,row in enumerate(csvreader):
                    if i == 0:
                        pass # ignore header on the first line
                    else:
                        TimeStampts.append(int(float(row[0])))
                        FeatureList.append(float(row[1]))
    #                plt.plot(np.array(TimeStampts), np.array(FeatureList))
    #                plt.title("Area [pixels] of " + os.path.basename(Folder))
    #                plt.show()

                TimeStamptsAll.append(TimeStampts)
                FeatureListAll.append(FeatureList)

        # write to asingle CSV file
        AllPotCSVFolder = os.path.join(RootPath, "csv")
        if not os.path.exists(AllPotCSVFolder):
            os.makedirs(AllPotCSVFolder)

        # assume the first pot has all timestamp
        LinuxTimeStamps = TimeStamptsAll[0]
        LinuxNoonTimeStamps = []
        HumanNoonTimeStamps = []
        Days = []
        for i,TimeStamp in enumerate(LinuxTimeStamps):
            TimeFloat = float(TimeStamp)/1000
            DateTime = datetime.datetime.fromtimestamp(TimeFloat)
            DateTimeNoon = datetime.datetime.combine(DateTime.date(), datetime.time(12, 00, 00))
            LinuxNoonTimeStamps.append(time.mktime(DateTimeNoon.timetuple()))
            HumanNoonTimeStamps.append(DateTimeNoon.strftime('%Y-%m-%d %H:%M:%S'))
            Days.append(DateTimeNoon.strftime('%Y-%m-%d'))
#            print(TimeStamp, " ", time.mktime(DateTimeNoon.timetuple()), " ", DateTimeNoon.strftime('%Y-%m-%d %H:%M:%S'))


        PotFeatureAll = []
        PotTimeStampAll = []
        for TimeStampts, FeatureList in zip(TimeStamptsAll, FeatureListAll):
            PotColFeature = []
            PotColTimeStamp = []
            ii = 0
            for i,(TimeStamp,PotFeature) in enumerate(zip(TimeStampts, FeatureList)):
                TimeFloat = float(TimeStamp)/1000
                DateTime = datetime.datetime.fromtimestamp(TimeFloat)
                DateTimeNoon = datetime.datetime.combine(DateTime.date(), datetime.time(12, 00, 00))
                if DateTimeNoon.strftime('%Y-%m-%d %H:%M:%S') == HumanNoonTimeStamps[ii]:
                    PotColFeature.append(PotFeature)
                    PotColTimeStamp.append(TimeStamp)
                elif DateTimeNoon.strftime('%Y-%m-%d %H:%M:%S') == HumanNoonTimeStamps[ii+1]:
                    PotColFeature.append("NaN")
                    PotColTimeStamp.append("NaN")
                    ii = ii+1
                    PotColFeature.append(PotFeature)
                    PotColTimeStamp.append(TimeStamp)
                else:
                    print("Found invalid data point")
                ii = ii + 1
            PotFeatureAll.append(PotColFeature)
            PotTimeStampAll.append(PotColTimeStamp)

        # Write feature file
        AllPotFeatureCSV = os.path.join(AllPotCSVFolder, "{}_{}.csv".format(Feature, Views[j]))
        PotColText = [os.path.basename(Folder).split("-")[1] for Folder in FoldersViews[j]]
        with open(AllPotFeatureCSV, "w") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(["TimeStamp (Linux time, sec)","TimeStamp (Forced at Noon)"] + PotColText)
            for i,(LinuxNoonTimeStamp,HumanNoonTimeStamp) in enumerate(zip(LinuxNoonTimeStamps, HumanNoonTimeStamps)):
                PotRowFeature = [PotColFeature[i] for PotColFeature in PotFeatureAll]
                PotRowFeature = [LinuxNoonTimeStamp,HumanNoonTimeStamp] + PotRowFeature
                csvwriter.writerow(PotRowFeature)

        # write time stamp file
        AllPotTimeStampCSV = os.path.join(AllPotCSVFolder, "timestamp_{}.csv".format(Views[j]))
        with open(AllPotTimeStampCSV, "w") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(["Day"] + PotColText)
            for i,Day in enumerate(Days):
                PotRowTimeStamp = [TimeStampts[i] for TimeStampts in PotTimeStampAll]
                PotRowTimeStamp = [Day] + PotRowTimeStamp
                csvwriter.writerow(PotRowTimeStamp)

