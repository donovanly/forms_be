from core.models import Form
from core.validation import validate_form
from rest_framework import serializers

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = [
            'form',
            'id',
            'name'
        ]
        read_only_fields = ['id']


    def validate_form(self, form):
        validate_form(form)
        return form
