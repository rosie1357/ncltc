
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

    def inpStays_hearts_drop_directs(self, hearts_df, group_cols, sort_cols):

        """ 
        Method inpStays_hearts_drop_directs to be called in main transform_inpStays
        Applies BR 4.1.1 to hearts:
            By CNDSID and ADMITDATE (sorted asc), identify the first record where prev_discharge_reason != Direct Discharge to Medical Visit
            and drop all records before that
        """

        # identify the first record by CNDSID/ADMITDATE where previous discharge reason is NOT Direct Discharge to Medical Visit (can be NA)

        hearts_df = hearts_df.sort_values(sort_cols).reset_index(drop=True).reset_index().rename(columns={'index':'new_index'})

        first_record = hearts_df[hearts_df['PREVDISCHRSN'].fillna('X') != 'Direct Discharge to Medical Visit'].groupby(group_cols).first().rename(columns={'new_index':'first_keep'})

        # Join back to full df to then drop any records in the same CNDSID/ADMITDATE group with index < selected index (ie first record(s) in group with Direct Discharge to Medical Visit)
        # NOTE! first_keep will never be set if there were no records by CNDSID with a value other than Direct Discharge to Medical Visit
        # must fill with max(hearts.index)+1 which will cause records to be dropped

        joined = pd.merge(hearts_df, first_record['first_keep'], how = 'outer', left_on=group_cols, right_on=group_cols)
        joined['first_keep'].fillna(max(hearts_df.index)+1, inplace=True)

        return joined.loc[joined['new_index']>=joined['first_keep']]

    def inpStays_hearts_drop_nonqual(self, hearts_df, drop_values):

        """ 
        Method inpStays_hearts_drop_nonqual to be called in main transform_inpStays
        Applies BR 4.1.2 to hearts:
            Drop all records where INSTCODE IN ('6','4','E','9'). 
        """

        return hearts_df.loc[~hearts_df['INSTCODE'].fillna('X').isin(drop_values)]

    def inpStays_hearts_bridge(self, hearts_df, group_cols, sort_cols, sort_asc):
        """
        Method inpStays_hearts_bridge to be called in main transform_inpStays
        Applied BR 4.2 to hearts:
            Bridge all remaining HEARTS stays where either 
                1) the previous discharge was due to medical reason for each CNDS, regardless of gap days, OR 
                2) the gap between records was 3 days or fewer 
        
        """

        # TODO: Can we move any bridging to common functions?

        hearts_df.sort_values(sort_cols, ascending=sort_asc, inplace=True)

        # lag DISCHDATE to compare to PREVDISCHDATE

        hearts_df['PRIOR_DISCHDATE'] = hearts_df.groupby(group_cols)['DISCHDATE'].shift(1)

        # identify records to bridge to prior record

        hearts_df['bridge'] = (hearts_df['PREVDISCHDATE']==hearts_df['PRIOR_DISCHDATE']) & \
                              ((hearts_df['PREVDISCHRSN']=='Direct Discharge to Medical Visit') | \
                              ((hearts_df['PREVDISCHRSN']!='Direct Discharge to Medical Visit') & (hearts_df['READMITDAYS']<4)))

        # lag bridge to identify the record it should be bridged WITH

        hearts_df['bridge_prior'] = hearts_df.groupby(group_cols)['bridge'].shift(-1).fillna(0)

        # create a final indicator to be used in cumsum to create the stay ID for bridging

        hearts_df['new_set'] = (hearts_df['bridge_prior']) & (hearts_df['bridge']==False).apply(lambda x: int(x))

        # now use cumsum on new_set to identify sets within group to bridge

        hearts_df['set_num'] = hearts_df.groupby(group_cols)['new_set'].cumsum()

        return hearts_df

    def transform_inpStays(self):

        # apply BR 4.1 on hearts using pipe!

        group_cols = ['CNDSID']
        sort_cols=group_cols + ['ADMITDATE']

        hearts = (self.df_dicts['rawdata.hearts'].
                  pipe(self.inpStays_hearts_drop_directs, group_cols=group_cols, sort_cols=sort_cols).
                  pipe(self.inpStays_hearts_drop_nonqual, ['6','4','E','9']).
                  pipe(self.inpStays_hearts_bridge, group_cols=group_cols, sort_cols=sort_cols + ['DISCHDATE'], sort_asc=[True, True, False])
                  )




        




