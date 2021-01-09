from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)
from rest_framework.views import APIView


class SecurityView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            'message': 'GET: Security.'
        }
        return Response(data=data, status=HTTP_200_OK)
