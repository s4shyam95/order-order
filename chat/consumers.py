import re
import json
import logging
from channels import Group, Channel
from channels.sessions import channel_session
from .models import Question, Answer, User

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    prefix = message['path'].strip('/')
    if prefix == 'conduct':
        Group('admin', channel_layer=message.channel_layer).add(message.reply_channel)
    else:
        Group('game', channel_layer=message.channel_layer).add(message.reply_channel)
    message.reply_channel.send({'text': json.dumps({'ping' : 'pong'})})


@channel_session
def ws_receive(message):
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
        print(message)
        log.debug('received', data)
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return

    if data:
        if data['type'] == 'join':
            u = User.objects.get_or_create(name=data['handle'])
            message.reply_channel.send({'text': json.dumps({'ping': 'pong'})})

        if data['type'] == 'answer':
            author = User.objects.get(name=data['handle'])
            question = Question.objects.get(id=data['question'])
            if len(question.answers.filter(by=author)) > 0:
                message.reply_channel.send({'text': json.dumps({'type': 'alert', 'message': 'Already Answered Question'})})
            elif question.hidden:
                message.reply_channel.send({'text': json.dumps({'type': 'alert', 'message': 'Question Not Open Yet'})})
            elif question.closed:
                message.reply_channel.send({'text': json.dumps({'type': 'alert', 'message': 'Question has been closed'})})
            elif ''.join(sorted(data['answer'])) != ''.join([str(x+1) for x in range(question.options)]):
                message.reply_channel.send({'text': json.dumps({'type': 'alert', 'message': 'Please enter a valid answer'})})

            else:
                answer = Answer(by=author, for_q=question, ans=data['answer'])
                answer.save()
                Group('admin', channel_layer=message.channel_layer).send({'text': json.dumps({'type': 'answer_admin', 'question':answer.for_q.id, 'by':answer.by.name, 'ans': answer.ans})})
                message.reply_channel.send({'text': json.dumps({'type': 'answer_response'})})

        if data['type'] == 'unlock_question':
            question = Question.objects.get(id=data['question'])
            question.hidden = False
            question.save()
            Group('game', channel_layer=message.channel_layer).send({'text': json.dumps({'type': 'unlock_question', 'question_id': data['question']})})

        if data['type'] == 'lock_question':
            question = Question.objects.get(id=data['question'])
            question.closed = True
            question.save()

        if data['type'] == 'show_answers':
            answers = None
            question = Question.objects.get(id=data['question'])
            if question.closed:
                message.reply_channel.send({'text': json.dumps({'type': 'alert', 'message': 'Answer not locked yet.'})})
            else:
                answers = [{'player':answer.by.handle, 'answer':answer.ans, 'score':answer.score()} for answer in question.answers]
                Group('game', channel_layer=message.channel_layer).send({'text': json.dumps({'type': 'show_answer', 'answers': json.dumps(answers), 'correct_answer': question.correct_answer})})

        if data['type'] == 'show_scores':
            scores_lis = [(player.total(), player.handle) for player in User.objects.all()]
            scores_lis.sort()
            scores_lis.reverse()
            scores = [{'score': score[0], 'player': score[1]} for score in scores_lis]
            Group('game', channel_layer=message.channel_layer).send({'text': json.dumps({'type': 'show_score', 'scores': scores})})

        if data['type'] == 'beat':
            message.reply_channel.send({'text': json.dumps({'ping': 'pong'})})

@channel_session
def ws_disconnect(message):
    Group('game', channel_layer=message.channel_layer).discard(message.reply_channel)
