/*
This file contains code to CREATE empty tables in the nctcl-rds-db database cluster.

See README.md in parent folder with instructions on how to generate the sql code and keep track
of changes/updates to tables.

*/

/* rawdata tables */

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
CNDSID VARCHAR(10) NOT NULL,
STATUS VARCHAR(100) NOT NULL,
STATUSBEGIN DATETIME NOT NULL,
STATUSEND DATETIME NOT NULL,
TCLIDATE DATE NULL,
BIRTHDATE DATE NULL,
LMEMCO VARCHAR(100) NULL,
TCLDID CHAR(5) NULL,
SUPERSTATUS VARCHAR(25) NULL,
HSN VARCHAR(10) NULL,
DHHSDETDATE DATE NULL,
MCAIDCOUNTY VARCHAR(100) NULL,
POPCAT VARCHAR(100) NULL,
GENDER VARCHAR(10) NULL,
RACE VARCHAR(100) NULL,
ETHNICITY VARCHAR(100) NULL,
EXTRACTDATE DATE NOT NULL,
PRIMARY KEY (CNDSID, STATUS, STATUSBEGIN, STATUSEND)
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

CREATE TABLE rawdata.nctracksProf
(
CNDSID VARCHAR(10) NOT NULL,
MBRID VARCHAR(7) NULL,
MBRID_ONE VARCHAR(7) NULL,
ALTMBRIDX VARCHAR(10) NULL,
ID_TYPE CHAR(1) NULL,
TCN CHAR(16) NOT NULL PRIMARY KEY,
CLMPDATE DATE NULL,
SVCBGN DATE NULL,
SVCEND DATE NULL,
PYRID SMALLINT NULL,
ADCOUNTYCODE CHAR(3) NULL,
RESCNTYCODE CHAR(3) NULL,
LNESTSCODE CHAR(1) NULL,
CLMHDRPDDATE DATE NULL,
DMHBNUM VARCHAR(10) NULL,
PAYCARRID VARCHAR(10) NULL,
LMEMCO VARCHAR(100) NULL,
LNERMBUNITAMT INT NULL,
LNECHARGEAMT FLOAT(10,2) NULL,
CLMLNENETPBLAMT FLOAT(10,2) NULL,
PAYPDAMT FLOAT(10,2) NULL,
AMTPD FLOAT(10,2) NULL,
PROCCODE VARCHAR(20) NULL,
SERVCODE VARCHAR(20) NULL
);

CREATE TABLE rawdata.nctracksInst
(
CNDSID VARCHAR(10) NOT NULL,
ALTMBRIDX VARCHAR(10) NULL,
ALTMBRID VARCHAR(12) NULL,
MBRID VARCHAR(7) NULL,
MBRID_ONE VARCHAR(7) NULL,
MBRRECSTSCD CHAR(1) NULL,
ALTSYSID_TYPE CHAR(1) NULL,
TCN CHAR(16) NOT NULL PRIMARY KEY,
SVCBGNDATE DATE NULL,
SVCENDDATE DATE NULL,
CLMHDRPDDATE DATE NULL,
PYRID SMALLINT NULL,
ADCOUNTYCODE CHAR(3) NULL,
RESCNTYCODE CHAR(3) NULL,
LNESTSCODE CHAR(1) NULL,
REVCODE VARCHAR(4) NULL,
LNERMBUNITAMT INT NULL,
LNECHARGEAMT FLOAT(10,2) NULL,
PAYPDAMT FLOAT(10,2) NULL,
DMHBNUM VARCHAR(10) NULL,
PAYCARRID VARCHAR(10) NULL,
LMEMCO VARCHAR(100) NULL,
AMTPD FLOAT(10,2) NULL,
SERVCODE VARCHAR(20) NULL
);

CREATE TABLE rawdata.cndsXwalkAlt 
(
CNDSID VARCHAR(10) NOT NULL,
ALTCNDSID CHAR(10) NOT NULL PRIMARY KEY,
BIRTHDATE DATE NULL,
DEATHDATE DATE NULL,
CNDSSEQNUM CHAR(1) NOT NULL
);

CREATE TABLE rawdata.CLIVE
(
TENANCYID VARCHAR(10) NOT NULL PRIMARY KEY,
HSN VARCHAR(10) NULL,
SUBSIDYTYPE VARCHAR(20) NULL,
TARGETFLAG VARCHAR(3) NULL,
LINKEDAMSEVENT VARCHAR(3) NULL,
LEGACYTYPE VARCHAR(3) NULL,
OUTOFHOUSING VARCHAR(4) NULL,
MOVEINEVENTDATE DATE NULL,
MOVEINAPPROVDATE DATE NULL,
INITLMEMCO VARCHAR(100) NULL,
CURRLMEMCO VARCHAR(100) NULL,
LEASESTARTDATE DATE NOT NULL,
MOVEINDATE DATE NULL,
MOVEOUTDATE DATE NULL,
MOVEOUTREASON VARCHAR(50) NULL,
CURRHOUSED VARCHAR(3) NULL
);

/* datamart tables */

CREATE TABLE datamart.ProfSvcs
(
CNDSID VARCHAR(10) NOT NULL,
SRCCNDSID VARCHAR(10) NOT NULL,
TCN CHAR(16) NOT NULL PRIMARY KEY,
CLMPDATE DATE NULL,
SVCBGH DATE NULL,
SVCEND DATE NULL,
LMEMCO VARCHAR(100) NULL,
SVCUNITS INT NULL,
PROCCODE VARCHAR(20) NULL,
SERVCODE VARCHAR(20) NULL,
MSRCODE VARCHAR(10) NOT NULL,
EXTRACTDATE DATE NOT NULL
);