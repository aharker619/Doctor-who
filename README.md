# Doctor-who
Project folder for CAPP30122 course for predicting ED wait times

Instructions for running project:

Install libraries if needed: django, googlemaps

To operate django web application:
1. Run server in django project. Within the project folder dw_site, run the command >python3 manage.py runserver
2. Open a browser and open http://127.0.0.1:8000/waittimes/
3. This will direct you to http://127.0.0.1:8000/waittimes/user_info which contains a form. Input your address, zipcode, and pain scale from 1 to 10. You must fill in the address and zipcode widget boxes. Press submit. There is also a link for an informational page on Urgent Care facilities.
4. If your zipcode was valid and found in our zipcode database you will load a results page. If your zipcode was not valid (ex. for non-valid zipcode = 00000) you will return a Validation Error with the message 'Please enter a valid zipcode'.
5. The results page will list up to five Emergency Departments that are within 800 km from your zipcode. These hospitals are sorted by total time which is the sum of the driving time (from Google Maps API) and the average wait time reported for the hospital. If there is no average wait time reported we use the median wait time for all wait time data we have through the NHAMCS dataset. If you have less than five hospitals there are either less than 5 hospitals in that radius or some hospitals were unable to gather driving directions through Google Maps API. (Note: if your address is not found using Google Maps geocode you will return Emergency Departments from only your zipcode)
6. If your area is experiencing extreme weather or has weather alerts an alert box will be at the top of your results page. This box will also contain a link to a new page describing the alerts. 
7. The alerts page lists the alerts for the zipcode. The alerts will first check WeatherUnderground API for National Weather Service alerts. If there are no alerts for your zipcode we will then check for other severe weather conditions through OpenWeatherMap API. This checks for severe or extreme weather descriptions as well as extreme wind chills and heat indicies. The alert from OpenWeatherMap will consist of the weather description, a wind chill warning with the calculated value, and/or a heat index warning with the calculated value. 


Code Structure:
- raw_data: 
    - This folder contains python code and csv files for data that were used to either create sqlite databases within django or our predicted wait time regression.
    - nhamcs data: Alyssa
        - Python Function:
            - nhamcs.py
        - Input Data:
            - nhamcsed*.csv is yearly data downloaded from the nhamcs database online, where * is the year
        - Output CSVs:
            - nhamcs_all_data.csv is all data from all years combined into one csv file. (stored in dw_site/waittimes) 
    - average wait time hospital data: Amir
        - Python Function:
            - Timely_Effective_Hospital_Data.py
        - Input Data:
            - Timely_and_Effective_Care_-_Hospital.csv is data downloaded from medicare.gov
        - Output CSV:
            - time.csv
    - general hospital data: Tianchu
        - Python Function:
            - hospital_info_datafilter.py
        - Input Data:
            - Hospital_General_Information.csv is data downloaded from medicare.gov
        - Output CSV:
            - HGI.csv
    - zipcode data: Alyssa
        - Python Function:
            - clean_zips.py
        - Input Data:
            - zipcodes.csv
            - 2015_Gaz_zcta_national.txt
        - Output CSV:
            - combined_zips.csv (stored in dw_site folder for loading data)
    - combine hospital information:Tianchu, Alyssa
        - Sqlite Function:
            - Create tables: create_tb.sql (Tianchu)
            - Query: combine_hosp.sql (Alyssa)
        - Input Data:
            - for create_tb.sql: time.csv, HGI.csv, combined_zips.csv, msa.csv, and states.csv
        - Output CSV:
            - ED.csv (stored in dw_site folder for loading data)
    - urgent care data: Alyssa
        - Python Function:
            - urgent_care.py
        - Input Data:
            - Urgent_Care_Facilities.csv
        - Output CSV:
            - urgent_care_data.csv (stored in dw_site folder for loading data)

- dw_site:
    - This folder contains the django project with the single application folder waittimes. Non-django generated files are be described below.
    - Python Function: Alyssa
        - load_data.py was used to load the data into the sqlite databases for django models
    - csv files to load data into databases, described above
- waittimes:
    - Non-django generated files are described below.
    - Python Functions:
        - closest_hosp.py: Alyssa
            - used to query for the 5 closest hospitals and closest urgent care as well as sort the hospitals with closest total time first
        - forms.py: Alyssa
            - holds form model for user input
        - get_distance_duration.py: Amir
            - used to get GoogleMaps API driving distances between user address and hospital
        - get_weather_alerts.py: Amir
            - used to get weather alerts from WeatherUnderground and/or OpenWeatherMaps API
        - regression.py: Tianchu
            - python functions for running regression
        - prediction.py: Tianchu
            - python functions for interfacing user input data with regression models and formatting results
        - finalized_model.sav: file for saving model for pickle
        - nhamcs_all_data.csv: for regression.py
    - templates: Alyssa
        - folder holds django templates as html files, namespace separated
            - user_info.html: user input page to begin application
            - resutls.html: list of hospitals and urgent care nearest to user
            - uc_fyi.html: Information about urgent care centers
            - weather.html: list of weather alerts for user's zipcode
- additional modeling files: Alyssa and Tianchu
    - nhamcs_model.py: (Alyssa) basic/beginning modeling functions Alyssa 
    - NHAMCS_analysis.ipynb: (Alyssa and Tianchu) initial exploration of data

Code Ownership Documentation
- "Direct copy": Generated by installed package (Django or other) and few edits made OR taken directly from specified source                                    
- "Modified": Generated by installed package (Django or other) and meaningful edits made OR heavily utilized template(s) provided by specified source
- "Original": Original code or heavily modified given structure    


