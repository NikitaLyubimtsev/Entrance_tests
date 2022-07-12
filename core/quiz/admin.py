from django.contrib import admin
from .models import *


class DirectionInLine(admin.TabularInline):
    model = Direction


class QuestionInLine(admin.TabularInline):
    model = Question


class AnswerInLine(admin.TabularInline):
    model = Answer


class DirectionAdmin(admin.ModelAdmin):
    inlines = [QuestionInLine]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]


class BlockAdmin(admin.ModelAdmin):
    inlines = [DirectionInLine]


admin.site.register(Block, BlockAdmin)
admin.site.register(Direction, DirectionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer)
admin.site.register(DirectionScore)
