from csv_config import *
import csv
import pandas as pd
from pandasControl import *

parseResume('node')
dataframe = pd.read_csv('table.csv')
print(sort(dataframe, 'salary'))