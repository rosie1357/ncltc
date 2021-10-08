
import pandas as pd
from itertools import starmap

from common.tasks.read_layout import read_layout
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
        
        dfs = starmap(lambda *x: DatabasetoDataFrame(*x).create_df(), [(read_layout(tbl.split('.')[-1]), tbl, self.db_params, self.log) for tbl in self.input_tables])
        
        return {name : df for name, df in zip(self.input_tables, dfs)}


    def transform_cndsXwalkAlt(self):

        # apply specific logic for cndsXwalkAlt (take original xwalk from wide to long)
            
        df = self.df_dicts['rawdata.cndsXwalk']
        
        alt_ids = list(filter(lambda x: (x.startswith('CNDSID')) & (~x.endswith('CNDSID')), df.columns))

        # transpose xwalk to take from wide to long, dropping any recs with a missing transposed value (alternate ID)

        xwalkt = pd.melt(df, id_vars=['CNDSID','BIRTHDATE','DEATHDATE'], value_vars=alt_ids).dropna(subset=['value'])

        # set any place-holder values of DTH_DT (1999-12-31) to null, create sequence number

        xwalkt['DEATHDATE'] = xwalkt['DEATHDATE'].apply(lambda x: '' if x == '1999-12-31' else x)

        xwalkt['CNDSSEQNUM'] = xwalkt.groupby(['CNDSID']).cumcount()+1

        return xwalkt.rename(columns={'value' : 'ALTCNDSID'}).sort_values(['CNDSID','CNDSSEQNUM'])

