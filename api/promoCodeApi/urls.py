from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.urls import path

urlpatterns = [
    path('promoCodes/<int:pk>/', views.UpdateCodes.as_view(), name='single-code'),
    path('promoCodes/', views.CodeList.as_view(), name='all-codes'),
    path('activeCodes/', views.ActiveCodeList.as_view(), name='active-codes'),
    # testCode requires three parameters; code, valid origin & destination name
    # [only letter,numbers,underscores,hyphens allowed in names]
    path('testCode/<slug:code>/<slug:origin>/<slug:destination>', views.test_code, name='test-code')
]

urlpatterns = format_suffix_patterns(urlpatterns)