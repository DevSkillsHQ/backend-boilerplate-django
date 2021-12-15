from django.http import response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_405_METHOD_NOT_ALLOWED, HTTP_409_CONFLICT
from .models import Option, Poll, Presentation, Question, Vote
from .serializers import PollSerializer, PresentationSerializer, TemplateSerializer


@api_view()
def ping(request):
    response = request.get('https://infra.devskills.app/api/interactive-presentation/ping')
    return Response(status=response.status)


@api_view(['POST'])
def templates(request):
    serializer = TemplateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    template = serializer.save()
    return Response({'template_id': template.template_id}, status=HTTP_201_CREATED)


@api_view(['POST'])
def presentations(request):
    serializer = PresentationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    presentation = serializer.save()
    return Response({'presentation_id': presentation.presentation_id}, status=HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def polls(request, pk, poll_id=None):
    if poll_id and request.method == 'POST':
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

    presentation = get_object_or_404(Presentation.objects.select_related(), pk=pk)
    poll = get_object_or_404(Poll, pk=poll_id) if poll_id else presentation.current_poll

    if request.method == 'GET':
        if not poll:
            return Response(status=HTTP_409_CONFLICT)

        serializer = PollSerializer(poll, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        if not poll:
            question = Question.objects.filter(template=presentation.template).earliest('id')
        else:
            question = get_object_or_404(Question.objects.filter(template=presentation.template, id__gt=poll.question_id))

        next_poll, created = Poll.objects.get_or_create(question=question)
        if created:
            next_poll.save()
        
        presentation.current_poll = next_poll
        presentation.save(update_fields=["current_poll"]) 

    serializer = PollSerializer(next_poll, context={'request': request})
    return Response(serializer.data, status=HTTP_201_CREATED)


@api_view(['POST'])
def votes(request, pk, poll_id):
    presentation = get_object_or_404(Presentation.objects.select_related(), pk=pk)
    poll = get_object_or_404(Poll.objects.select_related('question'), pk=poll_id)

    if poll != presentation.current_poll:
        return Response(status=HTTP_409_CONFLICT)

    option = get_object_or_404(Option.objects.filter(key=request.data.pop('selected_option_key'), question_id=poll.question_id))

    vote = Vote()
    vote.question_id = poll.question_id
    vote.selected_option_key = option
    vote.save()

    return Response(status=HTTP_201_CREATED)
