from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.db.models import Q

import math
from difflib import SequenceMatcher


class User(models.Model):
    name = models.CharField(max_length=19)
    datetime = models.DateTimeField(default=timezone.now)

    def total(self):
        return sum([ans.score() for ans in self.answers])

    class Meta:
        ordering = ('datetime',)

class Question(models.Model):
    correct_answer = models.TextField()
    options = models.IntegerField(default=5)
    datetime = models.DateTimeField(default=timezone.now)
    hidden = models.BooleanField(default=True)
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('datetime',)

class Answer(models.Model):
    by = models.ForeignKey(User, related_name='answers')
    for_q = models.ForeignKey(Question, related_name='answers')
    ans = models.CharField(max_length=10)
    datetime = models.DateTimeField(default=timezone.now)

    def score(self):
        if not self.for_q.closed:
            return 0
        correct = str(self.for_q.correct_answer)
        given = str(self.ans)
        s = SequenceMatcher(None, correct, given)
        lcs = ''.join([correct[block.a:(block.a + block.size)] for block in s.get_matching_blocks()])
        if len(lcs) <= self.for_q.options // 2:
            return 0
        score = 100
        correct = self.for_q.options
        while correct != len(lcs):
            score //= 2
            correct -= 1
        return score

    def total_score(self):
        if not self.for_q.closed:
            return 0
        answers = [(-1*answer.score(), answer.datetime, answer) for answer in self.for_q.answers.all()]
        score = self.score()
        if sorted(answers)[0][2] == self:
            score += 25

        return score

    class Meta:
        ordering = ('datetime',)
