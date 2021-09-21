

def convert_types(sqltype):
    
    """
        convert_types function to be applied to each row of the input df (table layouts)
        to map the SQL data types to valid types to be passed with SQL insert statements

        params:
            sqltype string: sqltype value (e.g. DATE, CHAR(2), SMALLINT)
            
        returns:
            string value for corresponding database type

    """

    if sqltype.startswith(('INT','SMALLINT','TINYINT')): 
        return 'longValue'
    
    elif sqltype.startswith(('VARCHAR','CHAR','DATE')):
        return 'stringValue'
    
    elif sqltype.startswith(('DECIMAL','FLOAT')):
        return 'doubleValue'