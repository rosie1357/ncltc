
import pandas as pd
from itertools import starmap
import os
from pathlib import Path

import common
from common.tasks.read_layout import read_layout
from common.utils.read_config import read_config
from common.utils.general_funcs import get_absolute_path
from common.classes.DatabasetoDataFrameClass import DatabasetoDataFrame

class DataTransform(object):
    """
    class DataTransform to run specific transformations for each analytic (non-raw) table
    
    """


    def __init__(self, analytic_tbl, input_tables, db_params, log, **kwargs):

        self.analytic_tbl, self.input_tables, self.db_params, self.log = analytic_tbl, input_tables, db_params, log

        # using DatabasetoDataFrame class, create dataframe for all tables in input_tables list
        # self.df_dicts = dictionary where key = name of database table and value = dataframe created from pull of table

        self.df_dicts = self.create_dataframes()

        # create df_to_db by calling transform method specific to analytic table

        self.df_to_db = eval(f"self.transform_{self.analytic_tbl}")()
        
        
    def create_dataframes(self):
        
        dfs = starmap(lambda *x: DatabasetoDataFrame(*x).create_df(), \
            [(read_layout(tbl.split('.')[-1], f"data_model_{tbl.split('.')[0]}"), tbl, tbl.split('.')[0], self.db_params, pull_columns, self.log) \
                for tbl, pull_columns in self.input_tables.items()])
        
        return {name : df for name, df in zip(self.input_tables, dfs)}


    def transform_cndsXwalkAlt(self):

        # apply specific logic for cndsXwalkAlt (take original xwalk from wide to long)
            
        df = self.df_dicts['rawdata.cndsXwalk']
        
        alt_ids = list(filter(lambda x: (x.startswith('CNDSID')) & (~x.endswith('CNDSID')), df.columns))

        # transpose xwalk to take from wide to long, dropping any recs with a missing transposed value (alternate ID)

        xwalkt = pd.melt(df, id_vars=['CNDSID','BIRTHDATE','DEATHDATE'], value_vars=alt_ids).dropna(subset=['value'])

        # set any place-holder values of DTH_DT (1999-12-31) to null

        xwalkt['DEATHDATE'] = xwalkt['DEATHDATE'].apply(lambda x: '' if x == '1999-12-31' else x)

        # drop duplicates by value (ALTCNDSID) - keep rec with highest value of CNDSID

        xwalkt = xwalkt[xwalkt['CNDSID'] == xwalkt.groupby('value')['CNDSID'].transform('max')]

        # add sequential rec count by CNDSID, return sorted df

        xwalkt['CNDSSEQNUM'] = xwalkt.groupby(['CNDSID']).cumcount()+1

        return xwalkt.rename(columns={'value' : 'ALTCNDSID'}).sort_values(['CNDSID','CNDSSEQNUM'])

    def transform_ProfSvcs(self):

        # read in mapper to get map between proc code and category

        config_path = get_absolute_path(common, 'config')

        proc_map = read_config(config_path / 'mapper.yaml')['PROC_MAPPING']



