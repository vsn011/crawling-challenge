import pandas as pd
import json
import glob
import os
import logging
pd.options.mode.chained_assignment = None


class Duplicate_finder:
    """Class for finding duplicate listings in jsonl files."""


    def __init__(self, path, key_columns):

        self.path=path
        self.key_columns=key_columns

    def read_jsonl(self):
        df_ = pd.DataFrame(index=None)
        extension = 'jsonl'
        os.chdir(self.path)
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

    def _get_df_with_duplicates(self):

        logging.info('finding duplicate listings')
        df=self.read_jsonl()
        
        #we drop those rows that have to many nan values in key columns
        df.dropna(subset=self.key_columns, thresh=4,inplace=True)
        duplicate_filter = df.duplicated(subset=self.key_columns, keep=False)
        df_duplicates = df[duplicate_filter]
        
        return df_duplicates

    @staticmethod
    def _get_key_column(df, key_columns):

        logging.info('creating unique key column')
        df=df
        key_columns=key_columns

        for c in key_columns:
            df[c] = df[c].astype(str)
        df['key']=df[key_columns].T.agg(','.join)
            
        return df

    def df_to_list(self):

        logging.info('creating list of duplicates')
        df_d=self._get_df_with_duplicates()

        df=self._get_key_column(df_d, self.key_columns)
        df = df[['id','platform','key']]
        grouped = df.groupby(df['key'])
        list_of_duplicates = []
        for key in df['key'].unique():
            temporary_df = grouped.get_group(key)[['platform','id']]
            l = temporary_df.to_dict('records')
            list_of_duplicates.append(l)
            
        return list_of_duplicates