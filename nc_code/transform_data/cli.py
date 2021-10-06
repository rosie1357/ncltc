"""
cli script to run transform_data from command line 
"""

import argparse
import os
from pathlib import Path

from common.tasks.create_config_class import create_config_class
from common.tasks.read_layout import read_layout
from common.classes.DatabaseInsertClass import DatabaseInsert
from common.utils.general_funcs import generate_logger, print_df_to_log
from common.classes.S3DataConnectClass import S3DataConnect

from .classes.DataTransformClass import DataTransform

def main(args=None):

    # add args and parse out - at cli must give:
    #   - name of table to insert into (will get table-specific info from analytic_tables_config)
    #   - optional param insert_type, default = overwrite
    #        only-once: means the data should only be loaded ONCE (do not want to mistakenly load e.g. ref data twice)
    #        overwrite: means ALL data currently in table should be deleted and new data inserted
    #        append: means should leave all data currently in table as is, and just append new data

    parser = argparse.ArgumentParser()
    parser.add_argument('--table_name', required=True)
    parser.add_argument('--insert_type', required=False, default='overwrite', choices=['only-once','overwrite','append'])
    args = parser.parse_args()
    
    table_name, insert_type = args.table_name, args.insert_type

    # create config class, reading in analytic_tables_config to add tables info to basic setup info

    config = create_config_class(**{'analytic_tables_config.yaml' : {'path' : Path(os.path.join(os.path.dirname( __file__ ),'utils')), 'outer_dict': table_name}})

    # create log - will create temp log then copy to bucket when complete

    log = generate_logger(logname = f"transform_data_{table_name}", init_message=f"CREATION OF table: {table_name}")

    # call read_layout function to return layout for given table as df
    
    layout_df = read_layout(table_name)

    # create s3 data class for given table - reads in raw data from s3 and converts to df following params given in tables_config
    # use layout to create dictionary of renames to map raw col to db col name
    
    DataTransform(analytic_tbl = table_name, input_tables = config.input_tables, db_params = vars(config)['DB_PARAMETERS'], log=log)
    """
    # create dbinsert class for given table, passing all needed params to connect to database from config class
    
    dbinsert = DatabaseInsert(df = df, layout_df = layout_df, tbl = table_name, db_params = vars(config)['DB_PARAMETERS'], insert_type=insert_type, log=log)

    # write any mismatches to log

    if len(dbinsert.mismatches) > 0:

        print_df_to_log(log = log, df = dbinsert.mismatches, message="All values that could NOT be inserted into database")

    # call batch execute method to insert to db table!

    dbinsert.sub_batch_execute_statement()

    # copy temp log to s3 bucket
    logpath = log.root.handlers[0].baseFilename

    S3DataConnect(config.DB_PARAMETERS['profile'], config.S3_BUCKETS['python_logs'], logpath, \
                  outfile='load_data/' + logpath.split('\\')[-1]).write_s3_obj()
    """