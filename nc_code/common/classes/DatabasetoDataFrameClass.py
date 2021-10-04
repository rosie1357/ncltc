"""
    DatabasetoDataFrame class to inherit from main Database class to use df and layout initial attributes
    to send query to pull records from database table and return pandas df
"""
import pandas as pd
import re
from common.utils.date_parser import parse_century

from .DatabaseClass import Database
from ..utils.db_util_funcs import convert_types

class DatabasetoDataFrame(Database):

    """
    DatabasetoDataFrame class - child of Database class to use layout for column types to create dataframe out of database table pull
    
    """

    def __init__(self, layout_df, tbl, db_params, log, pull_columns='*'):
        
        self.layout_df, self.tbl, self.db_params, self.log, self.pull_columns = layout_df, tbl, db_params, log, pull_columns
        super().__init__(db_params)

        self.records = self.pull_recs()

    def pull_recs(self):
        """
        Method pull_recs to issue query to pull all recs and select cols from database table

        response['records'] will return a list of lists of dictionaries, with each outer list = each database record
        """

        response = self.execute_statement(sql = f"select {','.join(self.pull_columns)} from {self.tbl}")
        return response['records']
