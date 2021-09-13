"""
    DatabaseInsert class to inherit from main Database class to use df and layout initial attributes
    to create insert statements for db table
"""
import pandas as pd
import re
from dateutil.parser import parse as parse_date

from .DatabaseClass import Database
from ..utils.db_util_funcs import convert_types

class DatabaseInsert(Database):

    """
    DatabaseInsert class - child of Database class to use to input dataframe and database table layout 
    and create insert statements and identify any mismatches, can then pass insert statements to batch execute
    
    """

    def __init__(self, df, layout_df, tbl, db_params, insert_type, log):
        
        self.df, self.layout_df, self.tbl, self.insert_type, self.log = df, layout_df, tbl, insert_type, log
        super().__init__(db_params)

        self.colmapping_dict = self.gen_layout_mapping()

        self.sql_parameter_sets, self.mismatches = self.gen_batch_inserts()

        self.sql_insert = self.create_sql_insert(tbl = self.tbl, cols=[col for col in self.colmapping_dict.keys()])

    def gen_layout_mapping(self):
        """
        method gen_layout_mapping to use df and layout_df passed attributes to
        create a dictionary mapping columns from df to db formats

        assumes the following:
            - self.layout_df has columns 'colname' and 'sqltype' that map input df/db columns to the database type 
                (e.g. DATE, CHAR(2), SMALLINT)

            - any columns that should map to the database layout on self.df have the same names 
                (e.g. if colname = 'CALYEAR' on self.layout_df, the column will also be named 'CALYEAR' on self.df)

        the method will identify all columns that are both in self.df.columns and listed in a record under 'colname' in self.layout_df and return
        a dictionary mapping colname to sqltype to pass to create_insert_statement() method
        
        
        """

        return {col : sqltype for col, sqltype in zip(self.layout_df['colname'], self.layout_df['sqltype']) if col in self.df.columns}

    def create_insert_statement(self, row):
    
        """
        method create_insert_statement to be applied to each row of the input df to then create
        SQL insert statements mapping df col to db col with row value

        params:
            row series: row of df to be inserted, auto-generated when applied to df with axis=1 call

        returns:
            insert list: list of all inserts for given row
            mismatches list: list of any mismatch types for given row that are set to null

        Notes:
            - if nan, must return syntax for null values
            - for all others, must attempt to convert to specified format. if cannot, set to null:
                - if date, must convert to string date format
                    - sometimes, dates read in as strings in format mm/dd/yyyy - also check for this if string. Add leading zeros to month/day
                - if string, must convert to string (applies to many fields that could be numbers, so dependent on what is read into dataframe from sheet)
                    - if CHAR or VARCHAR, must extract given length. if CHAR, must ensure matches exactly. if VARCHAR, must ensure not longer than length.
                - if decimal, must convert to float
                    - must ensure that integer part of value is not longer than allowed integer part of decimal
                - if int (longValue), must convert to int
            
        """

        insert = []
        mismatches = []
        
        for col, sqltype in self.colmapping_dict.items():
            
            # collapse input sqltypes to valid database type
            
            dbtype = convert_types(sqltype)
            
            if pd.isnull(row[col]) or str(row[col]) == '':
                dbtype = 'isNull'
                value = True
                
            else:
                try:
                    if sqltype == 'DATE':
                        if isinstance(row[col], str):
                            value = parse_date(row[col]).strftime('%Y-%m-%d')
                            
                        else:
                            value = row[col].strftime('%Y-%m-%d')
                
                    elif dbtype == 'stringValue':
                        value = str(row[col])

                        # if SQL type is VARCHAR or CHAR, check lengths and raise error if not conform

                        extract = re.match(r'(VARCHAR|CHAR)+\((\d+)\)',sqltype)
                        if extract is not None:
                            if (extract.group(1) == 'CHAR' and len(value) != int(extract.group(2))) | (extract.group(1) == 'VARCHAR' and len(value) > int(extract.group(2))):
                                raise ValueError

                    elif dbtype == 'longValue':
                        value = int(row[col])

                    elif dbtype == 'doubleValue':

                        # if currency read in as string, allow for removal of dollar sign before converting

                        if isinstance(row[col],str):
                            value = float(row[col].replace('$',''))
                            
                        else:
                            value = float(row[col])

                        # if DECIMAL, extract integer and decimal allowed values, and raise error if integer part of value is longer than allowed integer length

                        extract = re.match(r'DECIMAL\((\d+),(\d+)\)',sqltype)
                        if extract is not None:
                            if len(str(int(value))) > int(extract.group(1)) - int(extract.group(2)):
                                raise ValueError

                except:
                    mismatches.append({'Input column': col,
                                    'Input row': row.name+1,
                                    'Value': row[col], 
                                    'Database column': col,
                                    'Database format': sqltype})
                    dbtype = 'isNull'
                    value = True

            insert.append({'name':col, 'value': {dbtype: value}})

        return insert, mismatches

    def gen_batch_inserts(self):

        """
        gen_batch_inserts method to apply create_insert_statement row-wise to instance df to create list of 
        parameter sets to pass to batch execute, and list of mismatches to print to log
        
        """

        insertlists = self.df.apply(self.create_insert_statement, axis=1)

        mismatches = pd.DataFrame()
        sql_parameter_sets = []

        for i in range(len(insertlists)):
            sql_parameter_sets.append(insertlists[i][0])
            mismatch = insertlists[i][1]
            if len(mismatch) > 0:
                mismatches = pd.concat([mismatches, pd.DataFrame(mismatch)])

        return sql_parameter_sets, mismatches

    def sub_batch_execute_statement(self):
        """
        sub_batch_execute_statement method to call parent batch_execute_statement and pass created sql_insert and param sets
        must first check insert type to know how to insert
        
        """
        
        # if only-once, must check if any recs in table and if so, do NOT insert

        if self.insert_type == 'only-once':
            recs = self.get_rec_count(tbl=self.tbl)
            if recs > 0:
                self.log.info(f"{recs} already exist in database for given table - \nno new records inserted because insert_type == {self.insert_type}")

                return

        self.batch_execute_statement(sql = self.sql_insert, sql_parameter_sets = self.sql_parameter_sets)
        
        recs = self.get_rec_count(tbl=self.tbl)
        self.log.info(f"{recs} records inserted into database!")


