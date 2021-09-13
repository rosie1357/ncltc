"""
cli script to run load_data from command line 
"""

import argparse
import os
from pathlib import Path

from common.tasks.create_config_class import create_config_class
from common.tasks.read_layout import read_layout
from common.classes.DatabaseInsertClass import DatabaseInsert
from .classes.ReadRaw import ReadRawtoLoad

def main(args=None):

    # add args and parse out - at cli must give name of table to insert into (will get table-specific info from tables_config)

    parser = argparse.ArgumentParser()
    parser.add_argument('--table_name', required=True)
    args = parser.parse_args()
    
    table_name = args.table_name

    # create config class, reading in tables_config to add tables info to basic setup info

    config = create_config_class(**{'tables_config.yaml' : {'path' : Path(os.path.join(os.path.dirname( __file__ ),'utils')), 'outer_dict': table_name}})

    # call read_layout function to return layout for given table as df

    layout_df = read_layout(table_name)

    # create raw data class for given table - reads in raw data and converts to df following params given in tables_config

    raw_df = ReadRawtoLoad(table_name = table_name, **vars(config)).df

    # create dbinsert class for given table, passing all needed params to connect to database from config class

    dbinsert = DatabaseInsert(df = raw_df, layout_df = layout_df, tbl = 'calendarRef', db_params = vars(config)['DB_PARAMETERS'])

    # call batch execute method to insert to db table!

    dbinsert.sub_batch_execute_statement()



