'''
Function Purpose:
        Given two locations (home_location and away_location), function will 
            return the latitude, the longitude, the rounded-up distance as a string in km, 
            the exact distance as an integer in meters, the rounded-up time as 
            a string in hours and minutes, the exact time as an integer in seconds.

        Input:
            home_location: a string
            away_location: a string
            
        Return:
            A list: [text_distance, 
                    value_distance, text_duration, value_duration]

        Error Conditions:
            Distance error: 
                    When unable to drive from home_location to away_location,
                    returns -1, -1, -1, -1 as the respective values of 
                    text_distance, value_distance, text_duration, value_duration

            Geocode error:
                    When unable to locate the home_location and find latitude and longitude,
                    returns 100, 100 for latitude_home, longitude_home.
                    returns -1, -1, -1, -1 as the respective values of 
                    text_distance, value_distance, text_duration, value_duration
                    

Test Cases:

        Case 1:
            Both home_location and away_location are correct, and can be driven to.

            home_location = '1224 E 52nd Street Chicago'
            away_location = 'Harris School of Public Policy'


        Case 2: 
            Both home_location and away_location are correct, 
                but cannot drive from home_location to away location.

            home_location = '10th Street Bath Island Clifton Karachi Pakistan'
            away_location = 'Harris School of Public Policy'

        Case 3: 
            home_location is incorrect

            home_location = 'Malhota Pineapple House'
            away_location = 'Harris School of Public Policy'


Notes:
        1) Must import googlemaps to use this function:
                Use command: 'import googlemaps'
              
                    
        2) APIs used from Google:
            Distance-Matrix:
                https://developers.google.com/maps/documentation/distance-matrix/
            Geocoding:
                https://developers.google.com/maps/documentation/geocoding/intro
            
            Details: 
                2,500 free elements per day, calculated as the sum 
                    of client-side and server-side queries.
                Maximum of 25 origins or 25 destinations per request.
                100 elements per request.
                100 elements per second, calculated as the sum of 
                    client-side and server-side queries.
                
                
Further Progess:
                
        1) Need to write conditions for when API requests die.                    
        2) Look into Status Codes in both API documentation to account for error cases. 
'''
import googlemaps

def calculate_driving(user_address, user_zip, hosp_qs):
    '''
    Given a user address, calculate driving time to 5 hospitals in queryset

    Inputs:
        user_address: string
        hosp_qs: list of EmergencyDept objects
    Returns:
        hosp_qs: updated list with driving time in minutes
    '''
    for hosp in hosp_qs:
        hosp_address = ' '.join([hosp.address, hosp.city, hosp.state, hosp.zipcode])
        user_address = ' '.join([user_address, user_zip])
        driving_sec = get_distance_duration(user_address, hosp_address)
        # if the address is incorrect, recalculate with zipcode only
        if driving_sec is None:
            driving_sec = get_distance_duration(user_zip, hosp_address)
        hosp.driving_time = driving_sec / 60
    return hosp_qs

def get_distance_duration(home_location, away_location):
        
    distance_key = 'AIzaSyDyL6HDi1A2BYXGtdwVDZLSgYhkT6nt2cA'
    gmaps_distance = googlemaps.Client(key = distance_key)
    
    geocode_key = 'AIzaSyCnnrmNeGlB8Y7PLY7owGmewxpHH3_kDBU'
    gmaps_geocode = googlemaps.Client(key = geocode_key)
    
    geocode = gmaps_geocode.geocode(home_location)
    if geocode:
        latitude_home, longitude_home = geocode[0]['geometry']['location'].values()
    else:
        return None
    
    distance = gmaps_distance.distance_matrix(home_location, away_location)
    if distance['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS' or \
        distance['rows'][0]['elements'][0]['status'] == 'NOT_FOUND':
            text_distance, value_distance, text_duration, value_duration = -1, -1, -1, -1
    else:
        text_distance = distance['rows'][0]['elements'][0]['distance']['text']
        value_distance = distance['rows'][0]['elements'][0]['distance']['value']
        text_duration = distance['rows'][0]['elements'][0]['duration']['text']
        value_duration = distance['rows'][0]['elements'][0]['duration']['value']

    return value_duration
    
    
