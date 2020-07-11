from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.db.models import Q

import math
from difflib import SequenceMatcher


class User(models.Model):
    name = models.CharField(max_length=19)

    def total(self):
        return sum([ans.score() for ans in self.answers])

class Question(models.Model):
    correct_answer = models.TextField()
    options = models.IntegerField(default=5)
    datetime = models.DateTimeField(default=timezone.now)
    hidden = models.BooleanField(default=True)

    class Meta:
        ordering = ('datetime')

class Answer(models.Model):
    by = models.ForeignKey(User, related_name='answers')
    for_q = models.ForeignKey(Question, related_name='answers')
    ans = models.CharField(max_length=10)

    def score(self):
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
