from .models import *

from rest_framework import serializers

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['note_id', 'text', 'header', 'time']
        read_only_fields = ['time']
