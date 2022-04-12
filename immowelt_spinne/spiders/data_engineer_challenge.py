import pandas as pd
import os
import json
import glob
from file_reader import read_jsonl, df_to_list_of_dict, _get_df_with_duplicates, _get_list_of_duplicates_from_df
from itertools import product

path = 'C:\\Users\\38164\\Downloads\\jsonl\\'
key_columns = ['living_space','floor', 'rooms', 'zip_code', 'sale_type', 'price']




df = _get_df_with_duplicates(path, key_columns)

final_list=_get_list_of_duplicates_from_df(df)

print(len(final_list))









