from core.models import Form
from core.validation import validate_form
from rest_framework import serializers

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = [
            'created',
            'form',
            'id',
            'name',
            'updated',
        ]
        read_only_fields = [
            'created',
            'id',
            'updated',
        ]


    def validate_form(self, form):
        validate_form(form)
        return form
