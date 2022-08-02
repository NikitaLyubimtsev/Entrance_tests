from .models import *
from django.db.models import Sum

def block_one(bpk):
    direction_score = DirectionScore.objects.filter(block=bpk).aggregate(Sum('score'))
    print(direction_score)