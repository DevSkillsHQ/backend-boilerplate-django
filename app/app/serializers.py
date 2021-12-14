from rest_framework import serializers
from .models import Poll, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['key', 'value']


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['description', 'options', 'poll_id']

    options = OptionSerializer(source='option_set', many=True)
