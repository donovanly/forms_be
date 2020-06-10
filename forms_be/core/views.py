from core.models import Form
from core.serializers import FormSerializer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope
from rest_framework import viewsets


class FormViewSet(viewsets.ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope]

    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def perform_create(self,  serializer):
        return serializer.save(user=self.request.user)