# **NCTLC Code Base**

The NCTLC repo contains code to populate the AWS database and create measures for the North Carolina Transition to Community Living Initiative Services project.

This README will explain how to set up the local environment, add your AWS credentials, and submit the modules from the command line.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [**Local Setup**](#local-setup)
  - [**1. Environment Setup**](#1-environment-setup)
  - [**2. AWS Credentials**](#2-aws-credentials)
    - [**Create credentials empty files**](#create-credentials-empty-files)
    - [**Add project credentials**](#add-project-credentials)
    - [**Confirm credentials**](#confirm-credentials)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## **Local Setup**

### **1. Environment Setup**

This section details the local computer setup that needs to be done before running ANY module. This setup only needs to be done **once** per user (unless the user changes computers/installs/etc).

NOTE: These instructions assume python and Git are installed on your local computer, and local PATH variables are added accordingly. If they are not, create tickets for ITS to install them, following guidance in the [Data Science Handbook](https://mathematicampr.atlassian.net/wiki/spaces/DSEH/pages/456917237/How+to+Set+Up+Your+Computer).

This project uses pipenv to manage package depencies, and to add the main  **1115-public-comments** as a package to then easily call the individual modules using entry points.

To create the virtual environment using the [Pipfile](Pipfile), navigate to this folder in Git bash or terminal of your choice, and submit the following:

```bash
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

    - If you don't know where your home directory is, you can run the following command in Git bash to return the path (note that it's probably `C:/Users/USERNAME`):
```bash
echo $HOME
```
- In the home directory there may already be a subfolder called `/.aws`. If the folder is not there, create it. Make sure to include the '.' before 'aws'.

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