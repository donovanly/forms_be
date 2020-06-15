import json
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from oauth2_provider.models import get_access_token_model
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

def augment_request_auth(request):
    request.POST._mutable = True
    if request.data.get('grant_type') in ['', None]:
        request.data['grant_type'] = 'password'
    request.data['client_id'] = settings.AUTH_CLIENT_ID
    request.data['client_secret'] = settings.AUTH_CLIENT_SECRET
    request.POST._mutable = False


class LoginView(OAuthLibMixin, APIView):
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request, *args, **kwargs):
        augment_request_auth(request)
        url, headers, body, status = self.create_token_response(request)
        json_body = json.loads(body)
        
        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(token=access_token)
                app_authorized.send(sender=self, request=request,token=token)
                response_body = {'access_token': access_token}
                response_body['profile'] = {
                    'id': token.user.id,
                    'username': token.user.username,
                    'first_name': token.user.first_name,
                    'last_name': token.user.last_name,
                    'email': token.user.email
                }
        response = Response(response_body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response


class RegisterView(OAuthLibMixin, APIView):
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request):
        if request.auth is None:
            augment_request_auth(request)
            data = request.data
            data = data.dict()
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        user = serializer.save()

                        url, headers, body, token_status = self.create_token_response(request)
                        if token_status != 200:
                            raise Exception(json.loads(body).get("error_description", ""))
                        json_body = json.loads(body)
                        token = get_access_token_model().objects.get(token=json_body.get("access_token"))
                        response_body = {'access_token': json_body.get("access_token")}
                        response_body['profile'] = {
                            'id': token.user.id,
                            'username': token.user.username,
                            'first_name': token.user.first_name,
                            'last_name': token.user.last_name,
                            'email': token.user.email
                        }
                        return Response(response_body, status=token_status)
                except Exception as e:
                    return Response(data={"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
