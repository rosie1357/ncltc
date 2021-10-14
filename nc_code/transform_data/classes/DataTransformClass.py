
import pandas as pd
from itertools import starmap
import os
from pathlib import Path
from datetime import datetime

import common
from common.tasks.read_layout import read_layout
from common.utils.read_config import read_config
from common.utils.general_funcs import get_absolute_path
from common.utils.text_funcs import expand_range
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

    @staticmethod
    def add_extract_date(df):
        """
        Method add_extract_date to add column EXTRACTDATE as current date to df to be loaded - static method so can be used outside of class
        params:
            df: dataframe to add column to
        """

        return df.assign(EXTRACTDATE=datetime.today().strftime('%Y-%m-%d'))


    def merge_services_xwalk(self, services_tbl, how='inner', left_on='ALTCNDSID', right_on='CNDSID', right_rename='SRCCNDSID'):
        """
        Method merge_services_xwalk to do the generic merge of the services table to the xwalk by ALT ID on the xwalk and regular ID on the services table
        We want to keep the "master" CNDSID from the xwalk, and rename the ALT ID to SRCCNDSID.
        params:
            services_tbl (str): name of services table to use as key from self.df_dicts() to pull corresponding dataframe
            all other params are optional:
                how str: how to do join, default = inner
                left_on str: col on left table (cndsXwalkAlt) to merge on, default = ALTCNDSID
                right_on str: col on right table (services_tbl) to merge on, default = CNDSID
                right_rename str: name to rename right col to, default = SRCCNDSID

        
        """

        return pd.merge(left=self.df_dicts['rawdata.cndsXwalkAlt'], right=self.df_dicts[services_tbl].rename(columns={right_on : right_rename}), \
             how=how, left_on=left_on, right_on=right_rename).drop(columns=['ALTCNDSID'])


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

        # proc map is a dictionary with key = map category and value = list of either individual or ranges of proc codes.
        # must use expand_range common function to expand any ranges within keys to list out indiv values

        proc_map = {k : [j for i in list(map(expand_range, v)) for j in i] for k, v in proc_map.items()}

        # join services to xwalk (will then no longer need xwalk)

        df = self.merge_services_xwalk('rawdata.nctracksProf').rename(columns={'LNERMBUNITAMT':'SVCUNITS'})

        # add MSRCODE using proc_map - set to 'OTHER' if not found

        df['MSRCODE'] = df['PROCCODE'].apply(lambda x: ''.join([k for k, v in proc_map.items() if x in v]) or 'OTHER')

        # return df with EXTRACTDATE added

        return self.add_extract_date(df)

