# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 11:49:54 2017

@author: ee11ah
"""

import pandas as pd
from pandas import DataFrame
import datetime
import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
import os

BigNfiles = []
#read in big nipi data 
path = 'C:\\Users\\ee11ah\\Desktop\\allBN\\'
for root, dirs, files in os.walk(path):
    for file in files:
        #looks for big nipi files
        if file.startswith('bigN'):
            a =os.path.relpath(root) +'\\'
            bb = file
            a = a+bb
            print a