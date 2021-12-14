from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Poll, Option
from .serializers import PollSerializer


@api_view(['GET', 'POST'])
def polls(request, pk):
    if request.method == 'GET':
        #poll = get_object_or_404(Poll, presentation_id=pk)
        poll = Poll()
        poll.description = 'Ice cream'
        poll.save()

        option = Option()
        option.poll = poll
        option.key = 'Yes'
        option.value = 1
        option.save()

        option = Option()
        option.poll = poll
        option.key = 'No'
        option.value = 0
        option.save()

        serializer = PollSerializer(poll, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        return Response('ok')
