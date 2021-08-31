from common.tasks.create_config_class import create_config_class
from common.classes.DatabaseClass import Database
from common.classes.DatabaseInsertClass import DatabaseInsert


config_class = create_config_class()

db_class = DatabaseInsert(db_params = vars(config_class)['DB_PARAMETERS'])


print(db_class.execute_statement(sql='select * from rawdata.calendarRef'))