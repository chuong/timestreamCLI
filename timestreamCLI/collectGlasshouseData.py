# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 11:47:46 2014

@author: chuong
"""
from __future__ import print_function
import glob
import os
import csv
import datetime
import numpy as np
import matplotlib.pylab as plt

RootPath = "/home/chuong/Data/BVZ0038/BVZ0038-ProcessedPlantTSP-results/"
Views = ["SIDE", "TOP"]
FoldersViews = [glob.glob(os.path.join(RootPath, "*" + View)) for View in Views]
print("FoldersViews = ", FoldersViews)
for FoldersView in FoldersViews:
    for Folder in FoldersView:
        CSVFolder = os.path.join(Folder, "csv")
        AreaCSV = os.path.join(CSVFolder, "area.csv")
        with open(AreaCSV, "r") as csvfile:
            TimeStampts = []
            csvreader = csv.reader(csvfile, delimiter=',')
            AreaList = []
            for i,row in enumerate(csvreader):
                if i == 0:
                    pass # ignore header on the first line
                else:
                    TimeFloat = float(row[0])/1000
                    DateTime = datetime.datetime.fromtimestamp(TimeFloat)
                    TimeStampts.append(DateTime)
                    AreaList.append(float(row[1]))
            plt.plot(np.array(TimeStampts), np.array(AreaList))
            plt.title("Area [pixels] of " + os.path.basename(Folder))
            plt.show()