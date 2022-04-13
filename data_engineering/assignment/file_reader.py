import pandas as pd
import json
import glob
import os
import logging
pd.options.mode.chained_assignment = None

def read_jsonl(path):
    df_ = pd.DataFrame(index=None)
    path=path
    extension = 'jsonl'
    os.chdir(path)
    files = glob.glob('*.{}'.format(extension))
    logging.info("files to load: " + str(len(files)))
    

    for file in files:  
        appartments=[]
        with open(file, 'r') as json_file:
            json_list_home = list(json_file)
            logging.info("loading file: " + file)
        for json_str in json_list_home:
                result = json.loads(json_str)
                appartments.append(result)
        df = pd.DataFrame(appartments)
        df['platform'] = file.split('.')[0]
        frames = [df_, df]
        df_ = pd.concat(frames)
    logging.info('total rows loaded: ' + str(len(df_)))
    
    return df_

def _get_df_with_duplicates(df, key_columns):
    key_columns=key_columns
    df = df
    #we drop those rows that have to many nan values in key columns
    df.dropna(subset=key_columns, thresh=4,inplace=True)
    duplicate_filter = df.duplicated(subset=key_columns, keep=False)
    df_duplicates = df[duplicate_filter]
       
    return df_duplicates

def _get_key_column(df, key_columns):
    key_columns=key_columns
    df=df
    
    for c in key_columns:
        df[c] = df[c].astype(str)
    df['key']=df[key_columns].T.agg(','.join)
        
    return df

def df_to_list(df, key_columns):
    df=df
    key_columns=key_columns
    df=_get_key_column(df, key_columns)
    df = df[['id','platform','key']]
    grouped = df.groupby(df['key'])
    list_of_duplicates = []
    for key in df['key'].unique():
        temporary_df = grouped.get_group(key)[['platform','id']]
        l = temporary_df.to_dict('records')
        list_of_duplicates.append(l)
        
    return list_of_duplicates