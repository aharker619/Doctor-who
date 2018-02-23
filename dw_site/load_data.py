# this didn't work but if you put this into the shell it worked
# didn't try to run the file inside the shell without the django environ stuff

#csv_filepathname = '/home/student/Doctor-who/urgent_care_data.csv'
#django_project = 'home/student/Doctor-who/dw_site'

#import sys, os
#sys.path.append(django_project)
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from waittimes.models import UrgentCare
import csv

dataReader = csv.reader(open(csv_filepathname), delimiter= '|') 
for row in dataReader:
	if row[0] != 'ID':
		unit = UrgentCare()
		unit.provider_id = row[0]
		unit.name = row[1]
		unit.telephone = row[2]
		unit.address = row[3]
		unit.address2 = row[4]
		unit.city = row[5]
		unit.state = row[6]
		unit.zipcode = row[7]
		unit.lng = row[8]
		unit.lat = row[9]

		unit.save()

