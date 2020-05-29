from core.models import Form
from core.serializers import FormSerializer
from rest_framework import viewsets


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer