from django.test import TestCase
from .models import PromoCode
import datetime
from .serializers import PromoCodeSerializer
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

# model test case
class PromoCodeTest(TestCase):
    def setUp(self):
        self.expiry_date = datetime.date.today() + datetime.timedelta(days=3)
        self.code_1 =PromoCode(code='SB1', value=10000, radius_in_km=3,
                               expiry_date=self.expiry_date, venue_name='Design Hub Kampala')
        self.code_2 = PromoCode(code='SB2', value=5000, radius_in_km=6, expiry_date=self.expiry_date,
                                venue_name='Outbox Hub', code_status='Deactivated')

    def test_model_can_create_a_promo_code(self):
        old_count = PromoCode.objects.count()
        self.code_1.save()
        self.code_2.save()
        new_count = PromoCode.objects.count()
        self.assertNotEqual(old_count, new_count)

# views tests
class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        # add test data
        self.expiry_date = datetime.date.today() + datetime.timedelta(days=3)
        PromoCode.objects.create(code='SB1', value=10000, radius_in_km=3,expiry_date=self.expiry_date,
                                 venue_name='Design Hub Kampala')
        PromoCode.objects.create(code='SB2', value=5000, radius_in_km=6, expiry_date=self.expiry_date,
                                 venue_name='Outbox Hub', code_status='Deactivated')
        PromoCode.objects.create(code='SB3', value=15000, radius_in_km=6, expiry_date=self.expiry_date,
                                 venue_name='Acacia Mall')
        PromoCode.objects.create(code='SB4', value=5000, radius_in_km=3, expiry_date=self.expiry_date,
                                 venue_name='Makerere University', code_status='Deactivated')
        self.singleCode = PromoCode.objects.create(code='SB5', value=15000, radius_in_km=6, expiry_date=self.expiry_date,
                                    venue_name='Acacia Mall')

# test to show all codes are returned when request is made to promoCodes/ endpoint
class GetAllCodesTest(BaseViewTest):
    def test_get_all_codes(self):
        # hit the API endpoint
        response = self.client.get(reverse('all-codes'))
        # fetch the data from db
        codes = PromoCode.objects.all()
        serialized = PromoCodeSerializer(codes, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# test to show single code is returned when request is made to  promoCodes/:id endpoint
class GetSingleCodeTest(BaseViewTest):
    def test_get_valid_single_code(self):
        response = self.client.get(reverse('single-code', kwargs={'pk': self.singleCode.pk}))
        code = PromoCode.objects.get(pk=self.singleCode.pk)
        serializer = PromoCodeSerializer(code)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_code(self):
        response = self.client.get(reverse('single-code', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# test to show only active codes are returned when request is made to  activeCodes/ endpoint
class GetActiveCodesTest(BaseViewTest):
    def test_get_active_codes(self):
        response = self.client.get(reverse('active-codes'))
        codes = PromoCode.objects.filter(code_status='Active')
        serialized= PromoCodeSerializer(codes, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)




