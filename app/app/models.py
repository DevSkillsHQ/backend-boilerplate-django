import uuid
from django.db.models import Model, UUIDField, CharField, ForeignKey, CASCADE, Index, AutoField


class Poll(Model):
    id = AutoField(primary_key=True)
    presentation_id = UUIDField(default=uuid.uuid4, editable=False)
    poll_id = UUIDField(default=uuid.uuid4, editable=False)
    description = CharField(max_length=255)

    class Meta:
        indexes = [
           Index(fields=['presentation_id', 'poll_id',]),
        ]


class Option(Model):
    key = CharField(max_length=255)
    value = CharField(max_length=255)
    poll = ForeignKey(Poll, on_delete=CASCADE)


class Vote(Model):
    selected_option_key = ForeignKey(Option, on_delete=CASCADE)