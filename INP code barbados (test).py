# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 12:03:06 2017

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


#read in aps and met data
path = 'C:\Users\ee11ah\Desktop\Barbados_Data\\'
for root, dirs, files in os.walk(path):
    for file in files:
        if file.startswith('big'):
            a = file
            a
            
