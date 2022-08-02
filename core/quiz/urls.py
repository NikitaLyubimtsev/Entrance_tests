from django.urls import path
from .views import *


urlpatterns = [
    path('', LoginUser.as_view(), name='login'),
    path('quiz/', quiz_view, name='start-quiz'),
    path('quiz/block-data/', block_data, name='block-data'),
    path('quiz/<int:bpk>/<int:dpk>/save', direction_data_save, name='save-view'),
    path('quiz/<int:bpk>/<int:dpk>/data/', direction_data_view, name='direction-data-view'),
]