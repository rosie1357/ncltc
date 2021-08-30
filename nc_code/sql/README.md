# **SQL Scripts**

This folder of the repo contains SQL scripts to be run directly against the nctcl-rds-db database cluster.

## **1. Table Creation Code**

All scripts in the subfolder [create_tables](./create_tables) have been run in Query Editor to create the actual database tables.

The layouts for each of the database tables are in the data model here: `N:\Project\51164_NC_Olmstead\MA1\2. Data Management\05 Database Design\NC AWS Data Model.xlsx`.

The layout sheet is set up so that when cols A -- I are populated with the needed info for each column, formulas in col J will generate the SQL code to create each column. Col J then just needs to be copied and enclosed in an opening `'CREATE TABLE ...'` line with opening and closing parens.

Follow these steps to create a new database table:

1. Create a new sheet in the Excel data model file linked above, with the name of the sheet corresponding to the intended new table name. Use the *calendarRef* sheet as a template.
   - Note that the table must go into a specific schema within the database cluster. Cell A1 of the layout should specify the schema AND new table name in the form of `schemaname.tablename` (e.g. rawdata.calendarRef).

2. As mentioned above, col J will generate the SQL code to create each of the new columns. All of col J must just be sandwiched between the create table statement and opening and closing parens.

    For example, to create the table *calendarRef*, col J from the corresponding sheet just needs to be copied into a script with the additional SQL code appended:

    ```
    CREATE TABLE rawdata.calendarRef 
    (
    DATE DATE NOT NULL PRIMARY KEY,
    CALYEAR CHAR(4) NOT NULL,
    CALQTR CHAR(1) NOT NULL,
    CYYYYMM CHAR(6) NOT NULL,
    CALMM CHAR(2) NOT NULL,
    MONNAME CHAR(3) NOT NULL,
    CALYYYYMMDD CHAR(8) NOT NULL,
    FOMDATE DATE NOT NULL,
    EOMDATE DATE NOT NULL,
    SFY CHAR(4) NOT NULL,
    DAYSINMONTH CHAR(2) NOT NULL
    );
    ```

3. Before running the query in Query Editor to create the new table, create a new branch in the repo, copy the code into a script in [create_tables](./create_tables) and create a PR for review.

4. Once the code has been approved, you can run the code in Query Editor to actually create the table!

5. After the query runs successfully, submit the following command to return a description of every column in the table to ensure all looks correct:

   ```
    describe table schemaname.tablename
   ```

## **2. Table Update Code**

All scripts in the subfolder [update_tables](./update_tables) have been run in Query Editor to update the database tables.

These scripts are only needed if we find we need to alter an existing table. Reasons to do this would be if we found we needed to, e.g., make a text field longer after receiving new data with records that exceed the current length, or if we need to add a new column for additional analysis.

Follow these steps to update a database table:

1. Make all needed updates to the existing table layout, and add a row in the first 'Update Log' sheet with name, date, and description of updates.

2. Create the SQL code to make the needed update and add to a script in [update_tables](./update_tables). You can still use col J to generate some of the needed code, but will need to add the correct directions for what you are trying to do.

    For example, here is a line to add a datetime column `PROCESSINGDATE` to the existing table calendarRef, setting the new column on all existing records to NULL:

    ```
    alter table rawdata.calendarRef
    add PROCESSINGDATE DATETIME NULL;
    ```

3. So that the create tables SQL stays current, also update the existing code to create the table in [create_tables](./create_tables) to reflect all changes (i.e. so that if the table had to be recreated from scratch, it would match the new layout).

4. Follow the above instructions for creating a table, #3-5 to similarly create a PR, run the code, and confirm table looks as intended.