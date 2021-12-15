from django.db import transaction
from django.db.models import F
from django.db.models.aggregates import Count
from rest_framework import serializers
from .models import Poll, Option, Presentation, Question, Template, Vote


class PresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentation
        fields = ['template_id']

    template_id = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all())

    def create(self, validated_data):
        return Presentation.objects.create(template=validated_data.pop('template_id'))


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['key', 'value']


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['description', 'options', 'poll_id', 'votes']

    description = serializers.CharField(max_length=255, source='question.description')
    options = OptionSerializer(source='question.option_set', many=True)
    votes = serializers.SerializerMethodField(method_name='count_votes')

    def count_votes(self, poll: Poll):
        votes = Option.objects \
            .filter(question_id=poll.question_id) \
            .annotate(count=Count('vote')) \
            .values('key', 'count')
        return list(votes)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['description', 'options']

    options = OptionSerializer(source='option_set', many=True)


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['template_id', 'questions']

    questions = QuestionSerializer(source='question_set', many=True)

    def create(self, validated_data):
        with transaction.atomic():
            template = Template.objects.create()
            template.save()
            for question_data in validated_data['question_set']:
                question = Question()
                question.template = template
                question.save()
                for option_data in question_data['option_set']:
                    option = Option(**option_data)
                    option.question = question
                    option.save()
            return template
