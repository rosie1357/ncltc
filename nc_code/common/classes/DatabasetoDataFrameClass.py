"""
    DatabasetoDataFrame class to inherit from main Database class to use df and layout initial attributes
    to send query to pull records from database table and return pandas df
"""
import pandas as pd
from itertools import starmap

from .DatabaseClass import Database

class DatabasetoDataFrame(Database):

    """
    DatabasetoDataFrame class - child of Database class to use layout for column types to create dataframe out of database table pull
    
    """

    def __init__(self, layout_df, tbl, schema, db_params, pull_columns, log):
        
        self.layout_df, self.tbl, self.schema, self.db_params, self.pull_columns, self.log = layout_df, tbl, schema, db_params, pull_columns, log
        super().__init__(db_params)

        # if all columns are requested (pull_columns = *), will pull ALL columns - must identify from df layout

        if self.pull_columns == '*':
            self.pull_columns = list(self.layout_df['colname'])

        self.records = self.pull_recs()


    def pull_recs(self):
        """
        Method pull_recs to issue query to pull all recs and select cols from database table
        Because of limit to how much can be pulled at once, must first get the # of records in the table,
        then extract in chunks (similar to how the records are inserted with batch insert)

        response will return a list of lists of dictionaries, with each outer list = each database record
        """

        self.nrecs = self.get_rec_count(tbl = self.tbl, schema = self.schema)
        chunk=5000

        response=[]

        for i in range(0,self.nrecs,chunk):

            response = response + self.execute_statement(sql = f"select {','.join(self.pull_columns)} from {self.tbl} limit {i}, {chunk}", schema=self.schema)['records']

        return response

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
        
        # return one-rec dataframe with columns = input col names and values = values extracted from db
        
        return pd.DataFrame({col : [value] for col, value in zip(columns, values)})

    def create_df(self):
        """
        method create_df to iterate over list of list of records extracted from database and stack into full dataframe
        
        """

        df = pd.concat(list(starmap(self.create_df_record, [(rec, self.pull_columns) for rec in self.records]))).reset_index(drop=True)

        assert self.nrecs == df.shape[0], f"Count mismatch in creating df from {self.tbl} db table - expecting {self.nrecs} but pulled {df.shape[0]}"

        return df

