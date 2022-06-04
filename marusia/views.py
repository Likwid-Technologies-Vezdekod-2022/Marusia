from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class MarusiaCommandsView(APIView):
    def get(self, request):
        data = request.data
        return Response({'hz': 'hz'}, status.HTTP_200_OK)
