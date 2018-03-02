from waittimes.models import EmergencyDept, UrgentCare, ZipLocation

def find_closest(zipcode):
	'''
	Given a zipcode from ui, return the 5 closest hospitals and closest urgent care
	Input:
		zipcode: str
	Output:
		tuple: (query for hospitals, query for urgent care)
	'''
	if not zipcode:
		return ([], [])

	# convert zipcode to lat/long
	my_zip = ZipLocation.objects.get(zipcode = zipcode)
	lat = my_zip.lat
	lng = my_zip.lng

	# get queryset as list for hospitals
	hosp_qs = EmergencyDept.objects.rough_filter(lat, 
									lng).nearby(lat, lng, 800)
	if len(hosp_qs) > 5:
		hosp_qs = hosp_qs[:5]
	else: 
		hosp_qs = list(hosp_qs)

	# get queryset as list for urgent care
	uc_qs = UrgentCare.objects.rough_filter(lat, 
							   lng).nearby(lat, lng, 1000)
	if len(uc_qs) > 0:
		uc_qs = uc_qs[0]

	return (hosp_qs, uc_qs)

# https://stackoverflow.com/questions/15214992/it-is-necessary-to-use-geodjango-to-query-distances-in-django
# https://stackoverflow.com/questions/19703975/django-sort-by-distance/26219292#26219292
def sort_hospitals(hosp_qs):
	'''
	Given list of hospitals sort by total predicted time and driving time
	Inputs: 
		hosp_qs: list of hospitals as EmergencyDept objects
	Outpus:
		sort_hosp: sorted list of tuples (total time, EmergencyDept object)
	'''
	sort_hosp = []
	# store total time as tuple
	for hosp in hosp_qs:
		if hosp.driving_time != -1 / 60:
			time = hosp.driving_time + hosp.predicted_wait
		else:
			time = 9999
		sort_hosp.append((time, hosp))
	sort_hosp = sorted(sort_hosp)

	return sort_hosp
