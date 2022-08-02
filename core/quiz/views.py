from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
# from .models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import JsonResponse
from .calculation import *
from .forms import *


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'quiz/login.html'

    def get_success_url(self):
        return reverse_lazy('start-quiz')


def direction_view(request, pk):
    direction = Direction.objects.get(pk=pk)
    return render(request, 'quiz/direction.html', {'obj': direction})


def quiz_view(request):
    return render(request, 'quiz/quiz.html')


def block_data(request):
    qs = Block.objects.all()
    blocks = []
    for block in qs:
        directions = []
        for direction in block.get_directions():
            directions.append(direction.pk)
        blocks.append({str(block.pk): directions})
    return JsonResponse({
        'data': blocks
    })


def direction_data_view(request, bpk, dpk):
    block = Block.objects.get(pk=bpk)
    direct = []
    for d in block.get_directions():
        direct.append(d)
    direction = Direction.objects.get(pk=dpk)
    questions = []
    for q in direction.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
    })


def direction_data_save(request, bpk, dpk):
    if is_ajax(request=request):
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        direction = Direction.objects.get(pk=dpk)
        block = Block.objects.get(pk=bpk)
        # print(user, direction, sep='\n')

        score = 0

        for q in questions:
            a_select = request.POST.get(q.text)
            if a_select != "":
                q_a = Answer.objects.filter(question=q)
                for a in q_a:
                    if a_select == a.text:
                        if a.correct:
                            score += a.point
                #UserAnswer.objects.create(user=user, question=q, answer=a)
        #DirectionScore.objects.create(user=user, direction=direction, block=block, score=score)

        block_one(bpk)

        # Готовая функция включения подсчёта баллов в блоке
        # last_direction_in_block = Direction.objects.prefetch_related('block').filter(block=bpk).latest('pk').pk
        # if direction.pk == last_direction_in_block:
        #     sum = DirectionScore.objects.filter(direction.block.pk)
        #     print(sum)
        # else:
        #     print(direction.pk, last_direction_in_block, sep='\n')

        return JsonResponse({
            'passed': True,
        })
