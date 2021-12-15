import uuid
from django.db.models import Model, UUIDField, CharField, ForeignKey, CASCADE, Index, AutoField
from django.db.models.deletion import SET_NULL
from django.db.models.fields import BigIntegerField


class Template(Model):
    template_id = UUIDField(primary_key=True, default=uuid.uuid4)


class Presentation(Model):
    presentation_id = UUIDField(primary_key=True, default=uuid.uuid4)
    template = ForeignKey(Template, on_delete=CASCADE)
    current_poll = ForeignKey('Poll', on_delete=SET_NULL, null=True)


class Question(Model):
    template = ForeignKey(Template, on_delete=CASCADE)
    description = CharField(max_length=255)


class Option(Model):
    key = CharField(max_length=255)
    value = CharField(max_length=255)
    question = ForeignKey(Question, on_delete=CASCADE)


class Poll(Model):
    poll_id = UUIDField(primary_key=True, default=uuid.uuid4)
    question = ForeignKey(Question, on_delete=CASCADE)


class Vote(Model):
    selected_option_key = ForeignKey(Option, on_delete=CASCADE)