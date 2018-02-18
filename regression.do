clear all

* clear your previous memories.
 
set more off
* When I run codes, run all the way through. Don’t stop.

cd "/Users/tianchushu/Desktop/DR.Who/"
import delimited "nhamcs_data.csv"

summarize waittime
summarize arrtime

drop if fasttrak <0
drop if immedr < 0
drop if waittime <0
drop if arrtime <0
drop if painscale <0

gen jan = vmonth==1
gen feb = vmonth==2
gen mar = vmonth==3
gen apr = vmonth==4
gen may = vmonth==5
gen june = vmonth==6
gen july = vmonth==7
gen aug = vmonth==8
gen sept = vmonth==9
gen oct = vmonth==10
gen nov = vmonth==11
* generate the dummy variables for month

gen mon = vdayr==1
gen tue = vdayr==2
gen wed = vdayr==3
gen thur = vdayr==4
gen fri = vdayr==5
gen sat = vdayr==6
* generate the dummy variables for day of the week

gen workhr = 0
replace workhr = 1 if arrtime >= 800 & arrtime <= 2100

* arrtime between 8:00 to 21:00 is considered workhr.
* (12,656 real changes made)

gen immediate = immedr ==1
gen emergent = immedr ==2
gen urgent = immedr ==3
gen semiurgent = immedr ==4
gen nonurgent = immedr ==5
gen notriage = immedr ==0

gen regA = region ==1
gen regB = region ==2
gen regC = region ==3


reg waittime workhr painscale fasttrak msa jan feb mar apr may june july aug sept oct nov mon tue wed thur fri sat immediate  emergent urgent semiurgent nonurgent notriage 

