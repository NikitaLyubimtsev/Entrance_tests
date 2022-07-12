from django.views import generic
from django.shortcuts import render
from .models import *
from django.http import JsonResponse


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def direction_view(request, pk):
    direction = Direction.objects.get(pk=pk)
    return render(request, 'quiz/direction.html', {'obj': direction})


def direction_data_view(request, pk):
    direction = Direction.objects.get(pk=pk)
    questions = []
    for q in direction.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
    })


def direction_data_save(request, pk):
    if is_ajax(request=request):
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        direction = Direction.objects.get(pk=pk)

        score = 0

        for q in questions:
            a_select = request.POST.get(q.text)
            if a_select != "":
                q_a = Answer.objects.filter(question=q)
                for a in q_a:
                    if a_select == a.text:
                        if a.correct:
                            score += 1
            UserAnswer.objects.create(user=user, question=q, answer=a)
        print(score)
        DirectionScore.objects.create(user=user, direction=direction, score=score)

    return JsonResponse({'text': 'works'})
