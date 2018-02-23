/* Tianchu Shu */
/* msa.csv from https://www.census.gov/geographies/reference-files/time-series/demo/metro-micro/delineation-files.html*/
/* states.csv from https://github.com/jasonong/List-of-US-States/blob/master/states.csv */
/* zip_table data from http://federalgovernmentzipcodes.us/ */
CREATE TABLE time
  (provider_id varchar(10),
   hospital_name varchar(20),
   address varchar(100),
   city varchar(20),
   state varchar(2),
   zip_code varchar(9),
   county varchar(30),
   phone_number varchar(12),
   score integer,
   sample integer,
    PRIMARY KEY (provider_id));

.separator ","
.import time.csv time


CREATE TABLE hgi
 (provider_id varchar(10),
  zip_code varchar(9),
  hospital_overall_rating integer,

  FOREIGN KEY (provider_id)
    REFERENCES time (provider_id));

.separator ","
.import HGI.csv hgi

CREATE TABLE msa_table
  (CBSA_Code integer,
   Metropolitan_Division_Code integer,
   CSA_Code integer,
   CBSA_Title varchar(100),
   msa varchar(50),
   Metropolitan_Division_Title varchar(100),
   CSA_Title varchar(100),
   County varchar(100),
   State varchar(50),
   FIPS_State_Code integer,
   FIPS_County_Code integer,
   Central_Outlying_County varchar(20));

.separator ","
.import msa.csv msa_table

CREATE TABLE state_abbrv
  (fullname varchar(50),
   abbreviation varchar(2),

  FOREIGN KEY (fullname)
    REFERENCES msa_table (State));

.separator ","
.import states.csv state_abbrv

CREATE TABLE zip_table
  (zipcode varchar(9),
   zipcodetype varchar(20),
   city varchar(50),
   state varchar(50),
   locationtype varchar(50),
   lat real,
   lng real,
   location varchar(100),
   decommisioned varchar(10),
   tax integer,
   population integer, 
   wages integer);

.separator ","
.import free-zipcode-database-Primary.csv zip_table