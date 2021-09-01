from common.tasks.create_config_class import create_config_class
from common.classes.DatabaseInsertClass import DatabaseInsert


config = create_config_class()

import pandas as pd
import os

# hack way to test - read in calendar layout and df, then pass to DatabaseInsert class

layout = pd.read_excel(os.path.join(config.PATHS['db_design_dir'], config.FILES['data_model']), sheet_name='calendarRef', header=4)
print(layout)

df = pd.read_csv(os.path.join(config.PATHS['data_dir'], 'calendar.txt'), delimiter='\t')
print(df.head())

dbinsert = DatabaseInsert(df = df.head(5), layout_df = layout.rename(columns={'SQL Name' : 'colname', 'PostgreSQL Type' : 'sqltype'}), tbl = 'calendarRef',
                          db_params = vars(config)['DB_PARAMETERS'])


print(dbinsert.sql_parameter_sets)
print(dbinsert.sql_insert)

# call batch execute method to insert to db table

#dbinsert.batch_execute_statement()