"""
cli script to run load_data from command line 
"""

import argparse
import os
from pathlib import Path

from common.tasks.create_config_class import create_config_class
from common.tasks.read_layout import read_layout
from common.classes.DatabaseInsertClass import DatabaseInsert
from common.utils.general_funcs import generate_logger, print_df_to_log
from common.classes.S3DataConnectClass import S3DataConnect

from .classes.S3DataReadRawClass import S3DataReadRaw

def main(args=None):
    """
     add args and parse out - at cli must give:
       - name of table to insert into (will get table-specific info from tables_config)
       - optional param schema to give schema for given table, default = rawdata (all data loaded with this module should be inserted into rawdata)
            rawdata
            datamart
       - optional param insert_type, default = only-once
            only-once: means the data should only be loaded ONCE (do not want to mistakenly load e.g. ref data twice)
            overwrite: means ALL data currently in table should be deleted and new data inserted
            append: means should leave all data currently in table as is, and just append new data
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--table_name', required=True)
    parser.add_argument('--schema', required=False, default='rawdata', choices=['rawdata','datamart'])
    parser.add_argument('--insert_type', required=False, default='only-once', choices=['only-once','overwrite','append'])
    args = parser.parse_args()
    
    table_name, schema, insert_type = args.table_name, args.schema, args.insert_type

    # create config class, reading in tables_config to add tables info to basic setup info

    config = create_config_class(**{'tables_config.yaml' : {'path' : Path(os.path.join(os.path.dirname( __file__ ),'utils')), 'outer_dict': table_name}})

    # create log - will create temp log then copy to bucket when complete

    log = generate_logger(logname = f"load_data_{table_name}", init_message=f"LOAD OF TABLE: {table_name}")

    # call read_layout function to return layout for given table as df
    
    layout_df = read_layout(tblname = table_name, data_model = f"data_model_{schema}")

    # create s3 data class for given table - reads in raw data from s3 and converts to df following params given in tables_config
    # use layout to create dictionary of renames to map raw col to db col name
    
    raw_df = S3DataReadRaw(table_name = table_name, **{**vars(config), **{'renames' : dict(list(zip(layout_df['rawcol'],layout_df['colname'])))}}).df

    log.info(f"{raw_df.shape[0]} counts on raw table\n")
    
    # create dbinsert class for given table, passing all needed params to connect to database from config class
    
    dbinsert = DatabaseInsert(df = raw_df, layout_df = layout_df, tbl = table_name, schema = schema, db_params = vars(config)['DB_PARAMETERS'], insert_type=insert_type, log=log)

    # write any mismatches to log

    if len(dbinsert.mismatches) > 0:

        print_df_to_log(log = log, df = dbinsert.mismatches, message="All values that could NOT be inserted into database")

    # call batch execute method to insert to db table!

    dbinsert.sub_batch_execute_statement()

    # copy temp log to s3 bucket
    logpath = log.root.handlers[0].baseFilename

    S3DataConnect(config.DB_PARAMETERS['profile'], config.S3_BUCKETS['python_logs'], logpath, \
                  outfile='load_data/' + logpath.split('\\')[-1]).write_s3_obj()