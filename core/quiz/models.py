from django.db import models
from django.contrib.auth.models import User


class Block(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_directions(self):
        return self.direction_set.all()


class Direction(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_questions(self):
        return self.question_set.all()


class Question(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text

    def get_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    correct = models.BooleanField(default=False)
    point = models.IntegerField(default=0)

    def __str__(self):
        return f'question: {self.question}, answer: {self.text}, correct: {self.correct}'


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.question}'


class DirectionScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, blank=True, null=True)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.user} - {self.direction}'
