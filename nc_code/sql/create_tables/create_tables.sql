/*
This file contains code to CREATE tables in the nctcl-rds-db database cluster.

See README.md in parent folder with instructions on how to generate the sql code and keep track
of changes/updates to tables.

- will decide on naming conventions of scripts, etc

*/

-- ticket: https://mathematicampr.atlassian.net/browse/NCTCL-51
-- SQL query to create empty calendarRef table
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