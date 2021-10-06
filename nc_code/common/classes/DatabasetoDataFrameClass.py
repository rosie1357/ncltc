"""
    DatabasetoDataFrame class to inherit from main Database class to use df and layout initial attributes
    to send query to pull records from database table and return pandas df
"""
import pandas as pd
from itertools import starmap

from .DatabaseClass import Database
from ..utils.db_util_funcs import convert_types

class DatabasetoDataFrame(Database):

    """
    DatabasetoDataFrame class - child of Database class to use layout for column types to create dataframe out of database table pull
    
    """

    def __init__(self, layout_df, tbl, db_params, log, pull_columns=[]):
        
        self.layout_df, self.tbl, self.db_params, self.log, self.pull_columns = layout_df, tbl, db_params, log, pull_columns
        super().__init__(db_params)

        # if specific columns not requested (pull_columns is empty list), will pull ALL columns - must identify from df layout

        if len(self.pull_columns) == 0:
            self.pull_columns = list(self.layout_df['colname'])

        self.records = self.pull_recs()


    def pull_recs(self):
        """
        Method pull_recs to issue query to pull all recs and select cols from database table

        response['records'] will return a list of lists of dictionaries, with each outer list = each database record
        """

        response = self.execute_statement(sql = f"select {','.join(self.pull_columns)} from {self.tbl}")
        return response['records']

    @staticmethod        
    def create_df_record(response_rec, columns):
        """
        Static method (does not depend on class instantiation so can use outside class if desired)
        params:
            response_rec: list of one-rec dictionaries with key = database format (e.g. 'stringValue') and value = database value, EXCEPT in cases of nulls
                the response is a list of one-rec dictionaries, so must return value in the dictionary if it wasn't a dict with key = isNull and value = True (meaning null record) 
            columns:
                list of column names to pair with db extracted values

        returns:
            one-rec df
        
        """
    
        # extract values only from response, set nulls to pd.na
        # the response is a list of one-rec dictionaries, so must return value in the dictionary if it wasn't a dict with key = isNull and value = True (meaning null record)
        
        values = [list(value.items())[0][1] if not (list(value.items())[0][0]=='isNull') & (list(value.items())[0][1]==True) else pd.NA for value in response_rec]
        
        # return dictionary with input column names and values to append to all other recs
        
        return pd.DataFrame({col : [value] for col, value in zip(columns, values)})

    def create_df(self):
        """
        method create_df to iterate over list of list of records extracted from database and stack into full dataframe
        
        """

        return pd.concat(list(starmap(self.create_df_record, [(rec, self.pull_columns) for rec in self.records])))

