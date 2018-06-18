from rest_framework import status
from rest_framework.response import Response
from .models import PromoCode
from .serializers import PromoCodeSerializer
from rest_framework import generics
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from rest_framework.decorators import api_view
from polyline.codec import PolylineCodec
from geopy.exc import GeocoderTimedOut, GeocoderNotFound

# Create your views here.
#returns all codes
class CodeList(generics.ListCreateAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer

# returns only active codes
class ActiveCodeList(generics.ListCreateAPIView):
    queryset = PromoCode.objects.filter(code_status='Active')
    serializer_class = PromoCodeSerializer

# get, update, delete a code
class UpdateCodes(generics.RetrieveUpdateDestroyAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer

# return a code and polyline if code is valid and origin/destination are within venue radius
@api_view()
def test_code(request,code,origin,destination):
    # retrieve code if present or return error
    try:
        promo_code = PromoCode.objects.get(code=code)
    except PromoCode.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # remove dashes from origin and destination names/slug
    origin = origin.replace('-',' ')
    destination= destination.replace('-',' ')
    origin = origin.replace('_', ' ')
    destination = destination.replace('_', ' ')

    # get addresses for the origin, destination and venue
    geolocator = Nominatim()

    try:
        origin_location = geolocator.geocode(origin, timeout=10)
        print(origin_location)
    except (GeocoderTimedOut, GeocoderNotFound) as e:
        origin_error = "Error: geocode failed on input %s with message %s" % (origin, e.message)
        return Response({'Error': origin_error}, status=status.HTTP_504_GATEWAY_TIMEOUT)

    try:
        destination_location = geolocator.geocode(destination, timeout=10)
    except (GeocoderTimedOut, GeocoderNotFound ) as e:
        destination_error = "Error: geocode failed on input %s with message %s" % (destination, e.message)
        return Response({'Error': destination_error}, status=status.HTTP_504_GATEWAY_TIMEOUT)

    try:
        venue_location = geolocator.geocode(promo_code.venue_name, timeout=10)
    except (GeocoderTimedOut, GeocoderNotFound ) as e:
        venue_error = "Error: geocode failed on input %s with message %s" % (promo_code.venue_name, e.message)
        return Response({'Error': venue_error}, status=status.HTTP_504_GATEWAY_TIMEOUT)

    if origin_location and venue_location and destination_location:
        # calculate the distance between the origin,destination and venue
        origin_venue_distance = great_circle((venue_location.latitude,venue_location.longitude),
                                             (origin_location.latitude,origin_location.longitude)).kilometers
        destination_venue_distance = great_circle((venue_location.latitude,venue_location.longitude),
                                             (destination_location.latitude,destination_location.longitude)).kilometers

        # if code is still viable i.e active,not expired
        if promo_code.is_acceptable:
            # check if origin or destination is within radius of venue, if true return promo code data and encoded polyline
            if origin_venue_distance <= promo_code.radius_in_km or destination_venue_distance <= promo_code.radius_in_km:
                serializer = PromoCodeSerializer(promo_code)
                polyline = {'points': PolylineCodec().encode([(venue_location.latitude, venue_location.longitude),
                                                   (destination_location.latitude, destination_location.longitude)])}
                return Response({'code': serializer.data, 'polyline': polyline})
            else:
                error = {'Details': 'The promo code entered is invalid for given location'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            error = {'Details': 'Code entered is expired/deactivated'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)







