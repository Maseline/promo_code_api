from rest_framework import serializers
from .models import PromoCode


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields =('id', 'code', 'value', 'code_status', 'expiry_date', 'date_created', 'radius_in_km', 'venue_name')


