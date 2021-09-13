"""
    Main Database class to set database attributes and create generic client and execute methods
"""

import boto3

class Database(object):

    def __init__(self, db_params):

        # set all database parameters (passed in from config class) as class attributes

        for attrib, value in db_params.items():
            setattr(self, attrib, value)


    def gen_rds_client(self):

        """
        Method to generate RDS client to use in execute statements        
        
        """

        session = boto3.Session(profile_name=self.profile)
        return session.client('rds-data', region_name=self.region)

    def create_sql_insert(self, tbl, cols, schema='raw'):

        """
            method create_sql_insert to create sql insert statement to pass to batch_execute_statement, using input table and cols

            params:
                tbl string: database table name to insert into
                cols list: list of all columns to insert into 
                schema string: schema to pull from, default is raw. 
                    Options:
                        raw -> pulls from rawdata

            returns string with sql statement to pass to batch_execute_statement

        """

        return f"insert into {self.schema_names[schema]}.{tbl} ({', '.join(cols)}) values ({':' + ', :'.join(cols)})"


    def execute_statement(self, sql, schema='raw'):

        """
            execute_statement method to wrap around any sql code to pass to the database.
            will call the rds statement execute_statement

            params:
                sql string: sql code to execute
                schema string: schema to pull from, default is raw. 
                    Options:
                        raw -> pulls from rawdata

            returns:
                dictionary database response based on sql code

            example:
            
                execute_statement('select * from upl_db.tblSubmissionTracking')

            adapted from: https://aws.amazon.com/blogs/database/using-the-data-api-to-interact-with-an-amazon-aurora-serverless-mysql-database/

        """

        response = self.gen_rds_client().execute_statement(
            secretArn=self.db_credentials_secrets_store_arn,
            database=self.schema_names[schema],
            resourceArn=self.db_cluster_arn,
            sql=sql
        )

        return response

    def batch_execute_statement(self, sql, sql_parameter_sets, schema='raw'):

        """
            batch_execute_statement function to wrap around a sql statement and a two-dimensional array (set of lists) as params,
            which will call the rds statement batch_execute_statement to execute statements multiple times in a single API call

            params:
                sql string: sql code to execute
                sql_parameter_sets list: sql insert statements
                schema string: schema to pull from, default is raw. 
                    Options:
                        raw -> pulls from rawdata

            returns:
                dictionary database response based on sql code

            example of insert into tblProviderDetails (first three cols):

                sql = 'insert into upl_db.tblProviderDetails (RecordID, ProviderID, TemplateSubmissionId) values (:recordid, :providerid, :templatesubmissionid)'
                sql_parameter_sets = []
                for i in range(6,7):
                    entry = [
                            {'name':'recordid', 'value': {'doubleValue': i} },
                            {'name':'providerid', 'value': {'doubleValue': i*10} },
                            {'name':'templatesubmissionid', 'value': {'doubleValue': i*100} }
                    ]
                    sql_parameter_sets.append(entry)

                response = batch_execute_statement(sql, sql_parameter_sets)
                print(f'Number of records updated: {len(response["updateResults"])}')

            adapted from: https://aws.amazon.com/blogs/database/using-the-data-api-to-interact-with-an-amazon-aurora-serverless-mysql-database/

        """
        response = self.gen_rds_client().batch_execute_statement(
            secretArn=self.db_credentials_secrets_store_arn,
            database=self.schema_names[schema],
            resourceArn=self.db_cluster_arn,
            sql=sql,
            parameterSets=sql_parameter_sets
        )

        return response

    def get_rec_count(self, tbl):
        """
        Method get_rec_count return the record count from given table
        """

        response = self.execute_statement(sql = f"select count(1) from {tbl}")
        return list(response['records'][0][0].values())[0]