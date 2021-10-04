
import pandas as pd

from common.classes.DatabasetoDataFrameClass import DatabasetoDataFrame

class DataTransform(object):
    """
    class DataTransform to run specific transformations for each analytic (non-raw) table
    
    """


    def __init__(self, analytic_tbl, **kwargs):

        analytic_tbl = self.analytic_tbl

        # initialize with parents args

        super().__init__(self.layout_df, self.tbl, self.db_params, self.log, self.pull_columns)