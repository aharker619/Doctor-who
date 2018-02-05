#Tianchu Shu

CREATE TABLE time
  (Provider_ID varchar(10),
   Hospital_Name varchar(20),
   Address varchar(100),
   City varchar(20),
   State varchar(2),
   ZIP_Code varchar(9),
   Phone_Number varchar(12),
   Condition varchar(30),
   Score integer,
   Sample integer,
   Location varchar(150),
    PRIMARY KEY (Provider_ID));

.separator ","
.import time.csv time


CREATE TABLE hgi
 (Provider_ID varchar(10),
  ZIP_Code varchar(9),
  Hospital_overall_rating integer,

  FOREIGN KEY (Provider_ID)
    REFERENCES time (Provider_ID));

.separator ","
.import HGI.csv hgi


