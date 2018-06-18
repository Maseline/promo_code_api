from django.db import models
from datetime import date

# model for the promo code
STATUS_CHOICES = (('Active', 'Active'), ('Deactivated', 'Deactivated'))
class PromoCode(models.Model):
    code = models.CharField(max_length=255, blank=False)
    value = models.IntegerField(blank=False)
    radius_in_km = models.FloatField(blank=False)
    code_status = models.CharField(choices=STATUS_CHOICES, default='Active', max_length=50)
    expiry_date = models.DateField(blank=False)
    date_created = models.DateField(auto_now_add=True)
    venue_name = models.CharField(max_length=255)

    # code is acceptable if active and expiry date has not elapsed
    @property
    def is_acceptable(self):
        return self.code_status == 'Active' and self.expiry_date >= date.today()

    # function to return a human readable version of the model instance
    def __str__(self):
        return "{}".format(self.code)







