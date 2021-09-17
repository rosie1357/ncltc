/*
This file contains code to CREATE empty tables in the nctcl-rds-db database cluster.

See README.md in parent folder with instructions on how to generate the sql code and keep track
of changes/updates to tables.

*/

CREATE TABLE rawdata.calendarRef
(
CALDATE DATE NOT NULL PRIMARY KEY,
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

CREATE TABLE rawdata.cndsXwalk
(
CNDSID VARCHAR(10) NOT NULL PRIMARY KEY,
CNDSID1 CHAR(10) NULL,
CNDSID2 CHAR(10) NULL,
CNDSID3 CHAR(10) NULL,
CNDSID4 CHAR(10) NULL,
CNDSID5 CHAR(10) NULL,
CNDSID6 CHAR(10) NULL,
BIRTHDATE DATE NULL,
DEATHDATE DATE NULL
);

CREATE TABLE rawdata.tcldStatus
(
FQSTATUS VARCHAR(100) NULL,
TCLIDATE DATE NULL,
BIRTHDATE DATE NULL,
LMEMCO VARCHAR(100) NULL,
TCLDID CHAR(5) NULL,
STATUS VARCHAR(100) NOT NULL,
STATUSBEGIN DATETIME NOT NULL,
STATUSEND DATETIME NULL,
SUPERSTATUS VARCHAR(25) NULL,
CNDSID VARCHAR(10) NOT NULL,
PRIMARY KEY (CNDSID, STATUS, STATUSBEGIN)
);

CREATE TABLE rawdata.hearts
(
INSTCODE CHAR(1) NULL,
INSTNAME VARCHAR(100) NULL,
CNDSID VARCHAR(10) NOT NULL,
ADMITDATE DATE NOT NULL,
DISCHDATE DATE NULL,
READMITIND VARCHAR(3) NULL,
READMITDAYS SMALLINT(4) NULL,
PREVDISCHRSN VARCHAR(100) NULL,
PREVDISCHDATE DATE NULL,
GENDER CHAR(1) NULL,
HEARTSSTATUS CHAR(1) NULL,
BIRTHDATE DATE NULL,
MEDICAIDID VARCHAR(10) NULL,
CONSUMERID VARCHAR(10) NULL,
CLCASE VARCHAR(10) NULL,
APCODE VARCHAR(5) NULL,
RESIDCOUNTY VARCHAR(50) NULL,
LMEMCO VARCHAR(100) NULL,
DISCHREFERRAL VARCHAR(100) NULL,
DISCHRSN VARCHAR(150) NULL,
DIAG VARCHAR(10) NULL,
PRDIDS VARCHAR(2) NULL,
RESPCOUNTY VARCHAR(50) NULL,
DISCHLIVARR VARCHAR(100) NULL,
DISCHDESTCDE VARCHAR(10) NULL,
DISCHDEST VARCHAR(50) NULL,
DISCHTOCOUNTY VARCHAR(50) NULL,
LMEMCODISCHAFTERCARE VARCHAR(100) NULL,
PRIMARY KEY (CNDSID, ADMITDATE)
);