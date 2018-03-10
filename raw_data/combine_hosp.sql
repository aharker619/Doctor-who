/* Alyssa Harker */

/* Direct Copy: http://www.sqlitetutorial.net/sqlite-export-csv/ */
.mode csv
.headers on
.output ED.csv

/* Original Code */
SELECT time.provider_id, time.hospital_name, time.address, time.city, time.state,
time.zip_code, time.phone_number, time.score, time.sample, hgi.hospital_overall_rating,
zip_table.lng, zip_table.lat, counties.msa
FROM time LEFT OUTER JOIN hgi ON hgi.provider_id = time.provider_id
LEFT OUTER JOIN (
  SELECT County, msa, abbreviation
  FROM msa_table 
  JOIN state_abbrv ON state_abbrv.fullname = msa_table.State 
  WHERE msa_table.msa = 'Metropolitan Statistical Area')
AS counties ON (counties.abbreviation = time.state) AND
(time.county = counties.County COLLATE NOCASE)
LEFT OUTER JOIN zip_table ON time.zip_code = zip_table.zipcode;