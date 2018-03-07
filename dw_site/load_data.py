from waittimes.models import UrgentCare, EmergencyDept, PatientWaittime, ZipLocation
import csv
import os

def load_ed_data():
    with open('ED.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            unit = EmergencyDept()
            unit.provider_id = row[0]
            unit.name = row[1]
            unit.address = row[2]
            unit.city = row[3]
            unit.state = row[4]
            unit.zipcode = row[5]
            unit.phone_number = row[6]
            if row[7] == "Not Available" or not row[7]:
                unit.score = -1
            else:
                unit.score = row[7]
            if row[8] == "Not Available" or not row[8]:
                unit.sample = -1
            else:
                unit.sample = row[8]
            if row[9] == "Not Available" or not row[9]:
                unit.hospital_rating = -1
            else:
                unit.hospital_rating = row[9]
            unit.lng = row[10]
            unit.lat = row[11]
            if row[12]:
                unit.msa = row[12]
            else:
                unit.msa = ''

            unit.save()


def load_uc_data():
    with open('urgent_care_data.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter= '|')
        next(reader) 
        for row in reader:
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


def load_zip_data():
    with open('combined_zips.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            unit = ZipLocation()
            unit.zipcode = row[0]
            unit.lat = row[1]
            unit.lng = row[2]

            unit.save()