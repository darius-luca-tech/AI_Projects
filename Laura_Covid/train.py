import os

import numpy as np
import pandas as pd
import geopandas as gpd
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns

from shapely.geometry import Point
from tqdm import tqdm 
from sklearn.metrics import mean_squared_log_error
from datetime import datetime, timedelta

from tensorflow.keras import layers
from tensorflow.keras import Input
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping


#May God be with you
sns.set()

train_df = gpd.read_file("dataset_covid.csv")
# train_df["ConfirmedCases"] = train_df["ConfirmedCases"].astype("float") 
# print(type(train_df["ConfirmedCases"]))
print(type(train_df["ConfirmedCases"]))
# train_df = train_df[["Country_Region", "Date", "ConfirmedCases"]]
# train_df.head()

#VIN IMEDIAT BRB