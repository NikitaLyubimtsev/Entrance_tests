from django.urls import path
from .views import *


urlpatterns = [
    path('<int:pk>/', direction_view, name='direction-view'),
    path('', question_view, name='start-quiz'),
    path('<int:pk>/save', direction_data_save, name='save-view'),
    path('<int:pk>/data/', direction_data_view, name='direction-data-view'),
]