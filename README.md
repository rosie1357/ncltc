# **NCTLC Code Base**

The NCTLC repo contains code to populate the AWS database and create measures for the North Carolina Transition to Community Living Initiative Services project.

This README will explain how to set up the workspace environment, add your AWS credentials, upload the file layouts to s3, and submit the modules from the command line.

**Note**: There are currently two modules (*load_data* and *transform_data*), but additional modules for data processing/measure creation will be added when created.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [**Workspace Setup**](#workspace-setup)
  - [**1. Environment Setup**](#1-environment-setup)
  - [**2. AWS Credentials**](#2-aws-credentials)
    - [**Create credentials empty files**](#create-credentials-empty-files)
    - [**Add project credentials**](#add-project-credentials)
    - [**Confirm credentials**](#confirm-credentials)
- [**Database Layout Files to S3**](#database-layout-files-to-s3)
- [**Running the Modules**](#running-the-modules)
  - [**1. load_data**](#1-load_data)
  - [**2. transform_data**](#2-transform_data)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## **Workspace Setup**

### **1. Environment Setup**

All code must be run in Amazon Workspaces for security reasons. Once your workspace is set up, this will operate just like your local machine.

This section details the computer setup that needs to be done on your workspace before running ANY module. This setup only needs to be done **once** per user (unless the user changes computers/installs/etc).

You must be invited to Workspaces, and a workspace must also be assigned to you. Ask Shruthi Ramesh to do this for you if she has not already.

I forget what was already installed for me when I created my environment in Workspaces, but I either downloaded or saw the following were all there (I know I at least had to download Anaconda3):
- Anaconda3
- VSCode
- Git

Set up your environment and path variables following the DSE instructions:
 [Data Science Handbook](https://mathematicampr.atlassian.net/wiki/spaces/DSEH/pages/456917237/How+to+Set+Up+Your+Computer).

This project uses pipenv to manage package depencies, and to add the main  **nc_code** as a package to then easily call the individual modules using entry points.

Navigate to a local folder on your Workspace where you want to clone this repo and type the following in Git bash or terminal of your choice:

```bash
git clone https://github.com/mathematica-mpr/nctcl.git
```

To install pip and create the virtual environment using the [Pipfile](Pipfile), navigate to this folder and submit the following:

```bash
pip install pipenv
pipenv update
```

To enter the virtual env so that all commands given at the terminal are run in the virtual env, submit the following command:

```bash
pipenv shell
```

Note that each of the modules are added as entry points in [setup.py](setup.py) so they can be run in the virtual env with command shortcuts. See each module's section for specific instructions.

### **2. AWS Credentials**

All modules use the SDK boto3 to read data from and write data to the NC AWS account. Confirm access to the AWS account: [51164NC-TCLDev](https://mathematicaorg.awsapps.com/start)

If you do not have access, submit a ServiceNow ITS ticket specific to AWS account access, located here: [ITS ServiceNow AWS Account Help](https://mathematica.service-now.com/mpr?id=sc_cat_item&sys_id=84362c2fdb5d3340201ed498f4961992)

Once you are able to sign in, you will need to add credentials to the environment.

#### **Create credentials empty files** ####

- Go to the home directory on your local machine (using File Explorer or command line is fine)

    - If you don't know where your home directory is, you can run the following command in Git bash to return the path (note that it's probably `D:/Users/USERNAME`):
```bash
echo $HOME
```
- In the home directory create a folder called `/.aws`. Make sure to include the '.' before 'aws'.

- Within the `/.aws` folder, create two new files called `credentials` and `config` (no file extension). You can do this two ways:

  - Manually save empty Notepad files with those names, OR

  -  Create from the command line by running the following in the `/.aws` folder:
  ```bash
  touch credentials
  touch config
  ```

- Open the `config` file and add the following lines (I always open these in Notepad, but any text editor is fine):

```bash
[default]

region = us-east-2
```

#### **Add project credentials** ####

- To finish setting up the credentials file, return to the [51164NC-TCLDev](https://mathematicaorg.awsapps.com/start) in your browser

  - Select 'Command Line or Programmatic Access'. This will display the AWS environmental variables you need to copy into your credentials file.

  - Click in the box for Option 2 ('Add a Profile to your AWS credentials file') to copy the credentials listed.

  - Copy all four lines into the `/.aws/credentials` file on your local machine.

  Your credentials file should look like this (with each XXXX replaced with the actual value copied in)
  ```
  [838494257041_Project_Developer]
  aws_access_key_id=XXXX
  aws_secret_access_key=XXXX
  aws_session_token=XXXX
  ```

- The aws\_access\_key\_id never changes, but the aws\_secret\_access\_key and aws\_session\_token change with each login, and automatically expire after 10 hours. You will need to follow these same steps as above to update the credentials file with the new credentials each time you log into the AWS account after 10 hours.

#### **Confirm credentials** ####

- We will use the AWS CLI tool (`awscli`) at the command line to check the credentials were correctly picked up by the files created above. Submit the following two lines to:
  - Install the awscli package if not already installed
  - Retrieve the AWS credentials for a specified profile you have added to your credentials file
    -  The below command requests the credentials for the production account profile `838494257041_Project_Developer`.

```bash
pip install awscli
aws configure --profile 838494257041_Project_Developer
```

 See [AWS docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) for more details on using `awscli`.

The default values returned should be the new credentials (with all but the last four characters masked).

## **Database Layout Files to S3**

The modules read the database layout files from S3. The files are mainly updated by Kent/analysts on N here: `N:\Project\51164_NC_Olmstead\MA1\2. Data Management\05 Database Design`.

The two files are:
- `NC AWS Data Model.xlsx` (raw data)
- `NC AWS Data Mart Data Model.xlsx` (transformed **'datamart'** data)

I don't know how much more they will be changed, but if you see they have been, upload the new versions to the [data-models bucket](https://s3.console.aws.amazon.com/s3/buckets/nctlc-data-models?region=us-east-1&tab=objects).
Note the bucket is version-controlled so you do not need to worry about overwriting versions - you can always get them back!

## **Running the Modules**

### **1. load_data**

The module load_data is the first main module, which will load all raw data submitted by the state. It retrieves the data from S3, performs the minimum cleaning needed to be able to get into the database, and then inserts into that file-specific table in the database.

**NOTE**: There is a set of SQL code with a separate README in the [sql](nc_code/sql) subfolder. This subfolder describes how to create/update each table in the database, which must happen before data load.

To load a raw data file to the database, you must do two things:
1. Add an entry to the [tables_config.yaml](nc_code/load_data/utils/tables_config.yaml) file for the given file. See the yaml file for examples of files that have been loaded.

    As an example, here is the entry for the calendar reference file, which was inserted into the **calendarRef** table in the database:

    ```
    calendarRef:
      bucket_ref: raw_data
      infile: Calendar.txt
      file_type: csv
      readin_kwargs:
        delimiter: '\t'
        dtypes:
          CALMM: str
    ```

    The outermost key is the name of the target table. The only other required parameters are:
      - bucket_ref: reference name for bucket that contains the raw data
      - infile: name of raw data in S3 bucket
      - file_type: file type (currently only allow csv, will update to allow .sas7bdat when the state submits)

    There are optional parameters that can be specified in `readin_kwargs`, which will all be passed as additional parameters to the file read in command (e.g. pd.read_csv()). In the example above, the Calendar.txt file had to be read in as tab-delimited with the column CALMM specified as string to retain leading zeros.

2. Submit at the command line using the entry point defined in [setup.py](setup.py), with one required (*--table_name*) and two optional (*--schema, --insert_type*) arguments:

    ```bash
    load_data --table_name calendarRef --schema raw --insert_type overwrite
    ```
    See the [cli.py](nc_code/load_data/cli.py) script for more information on the parameters.

    After each run, a log will be generated in the [S3 logs bucket](https://s3.console.aws.amazon.com/s3/buckets/nctlc-python-logs?region=us-east-1&prefix=load_data/&showversions=false) in the 'load_data' key (subfolder).

    For the FINAL run of the table, move the log to the 'final' subfolder within the above subfolder.

### **2. transform_data**

The module transform_data is the second main module, which reads in tables already created in the database to do specific transforms/apply business rules (i.e. not simply extracting and loading raw data). Almost all of the transformed tables will be inserted into the `datamart` schema. An exception is the table `cndsXwalkAlt`, which is created in the rawdata schema. This table is simply a transpose of `cndsXwalk`.

**NOTE**: There is a set of SQL code with a separate README in the [sql](nc_code/sql) subfolder. This subfolder describes how to create/update each table in the database, which must happen before data load.

To perform the transformations and load the transformed file to the database, you must do three things:
1. Add an entry to the [analytic_tables_config.yaml](nc_code/transform_data/utils/analytic_tables_config.yaml) file for the given file. See the yaml file for examples of files that have been loaded.

    As an example, here is the entry for the transposed CNDS xwalk file, which was inserted into the **cndsXwalkAlt** table in the database:

    ```
    cndsXwalkAlt:
      input_tables:
        - rawdata.cndsXwalk
    ```

    The outermost key is the name of the target table. The only other required parameter is:
      - input_tables: a list of ALL input tables (in the form of schema.tablename) that must be pulled from the database and converted to dataframes to then perform all transformations to create the new analytic table.

2. Add a method to [DataTransformClass.py](nc_code/transform_data/classes/DataTransformClass.py) with code to do all transformations and create analytic table from inputs.
    - The method must be named `f"transform_{analytic_tbl}"()`.
    - The input dataframes to be used in the method are created in the init method `self.create_dataframes()`. This method pulls all tables listed in `input_tables` above from the database and creates dataframes. The return from this method is a dictionary where the key = name of table and value = dataframe. This dictionary of tables will be used in the transform method.
    - The return from this method must be a dataframe in the form of the analytic table to insert into the database.

3. Submit at the command line using the entry point defined in [setup.py](setup.py), with one required (*--table_name*) and two optional (*--schema, --insert_type*) arguments:

    ```bash
    transform_data --table_name calendarRef --schema datamart --insert_type overwrite
    ```
    See the [cli.py](nc_code/transform_data/cli.py) script for more information on the parameters.

    After each run, a log will be generated in the [S3 logs bucket](https://s3.console.aws.amazon.com/s3/buckets/nctlc-python-logs?region=us-east-1&prefix=transform_data/&showversions=false) in the 'transform_data' key (subfolder).

    For the FINAL run of the table, move the log to the 'final' subfolder within the above subfolder.