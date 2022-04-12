import pandas as pd
import json
import glob
import os
from itertools import product


def read_jsonl(path):
    df_ = pd.DataFrame(index=None)
    path=path
    extension = 'jsonl'
    os.chdir(path)
    files = glob.glob('*.{}'.format(extension))
    print("files to load: " + str(len(files)))
    

    for file in files:  
        appartments=[]
        with open(file, 'r') as json_file:
            json_list_home = list(json_file)
            print("loading file: " + file)
        for json_str in json_list_home:
                result = json.loads(json_str)
                appartments.append(result)
        df = pd.DataFrame(appartments)
        df['platform'] = file.split('.')[0]
        frames = [df_, df]
        df_ = pd.concat(frames)
    print('rows loaded: ' + str(len(df_)))
    
    return df_


def df_to_list_of_dict(df):
    df=df
    list_of_lists = []
    for index, row in df.iterrows():
        small_list = []
        row = row.to_dict()
        small_list.append(row)
        list_of_lists.append(small_list)

    return list_of_lists


def _get_df_with_duplicates(path, key_columns):
    
    path=path
    key_columns=key_columns
    df = read_jsonl(path)
    
    #here we extract duplicated listings based on the given columns into a separate dataframe; 
    #all duplicates are stacked on top of eachother without duplicate pairs
    duplicate_filter = df.duplicated(subset=key_columns, keep=False)
    df_duplicates = df[duplicate_filter]
    
    #in order to get duplicate pairs we inner join duplicate subset with the starting dataframe
    #by doing so we don't just join duplicate listing with their coresponding duplicates but also to themselves, that is why we need to filter them out 
    duplicates = df.merge(df_duplicates, how = 'inner', on=key_columns, indicator=False)
    
    
    #next we prepare the dataframe for the requested file format
    
    df_final=duplicates[['platform_x', 'id_x', 'platform_y', 'id_y']]
    df_final=df_final[df_final['id_x'] != df_final['id_y']]
    
    return df_final


def _get_list_of_duplicates_from_df(df):
    df=df
    df1=df[['platform_x','id_x']]
    df2=df[['platform_y','id_y']]
    df1.rename(columns={'platform_x': 'platform', 'id_x':'id'}, inplace=True)
    df2.rename(columns={'platform_y': 'platform', 'id_y':'id'}, inplace=True)
    
    list1=df_to_list_of_dict(df1)
    list2=df_to_list_of_dict(df2)

    final_list = []
    for (a, b) in zip(list1, list2):
        l =  [a[0],b[0]]
        final_list.append(l)
    
    return final_list