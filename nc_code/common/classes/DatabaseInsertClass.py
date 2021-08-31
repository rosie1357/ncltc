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
    and create insert statements to be passed to batch execute to insert multiple records into database table
    
    """

    def __init__(self, df, layout, db_params):
        self.df, self.layout = df, layout
        super().__init__(db_params)

    def create_inserts(row, colmapping):
    
        """
        create_inserts method to be applied to each row of the input df to then create
        SQL insert statements mapping df col to db col with row value

        params:
            row series: row of df to be inserted, auto-generated when applied to df with axis=1 call
            colmappings dict: dictionary with mapping of df col to db col with format types
                the colmappings dict is structured as follows:
                    key = column name (assumes df column and db column have same name)
                    value = database SQL type

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
        
        for col, sqltype in colmapping.items():
            
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
                                    'Input row': row['rownum'],
                                    'Value': row[col], 
                                    'Database column': col,
                                    'Database format': sqltype})
                    dbtype = 'isNull'
                    value = True

            insert.append({'name':col, 'value': {dbtype: value}})

        return insert, mismatches