import random
import string
from django.db import transaction
from django.shortcuts import render, redirect
import haikunator
from .models import Question, User, Answer


def chat_room(request):
    """
    Room view - show the room, with latest messages.

    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """

    # We want to show the last 50 messages, ordered most-recent-last

    questions = Questions.objects.all()
    players = User.objects.all()

    return render(request, "chat/room.html", {
        'questions': questions,
        'players': players,
    })


def admin_room(request):
    questions = Question.objects.all()
    return render(request, "chat/admin.html", {
        'questions': questions,
    })
