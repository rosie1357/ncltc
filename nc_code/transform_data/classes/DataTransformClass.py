
from collections import defaultdict
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

        # using DatabasetoDataFrame class, create dataframe from all tables in input_tables list

        dfs = starmap(lambda *x: DatabasetoDataFrame(*x).create_df(), [(read_layout(tbl.split('.')[-1]), tbl, self.db_params, self.log) for tbl in self.input_tables])
        