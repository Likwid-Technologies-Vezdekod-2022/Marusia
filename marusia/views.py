from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class MarusiaCommandsView(APIView):
    def get(self, request):
        data = request.data
        response = {
                "response": {
                    "text": "Неизвестная команда",
                    "tts": "неизвестная команда",
                    "end_session": True
                },
                "version": "1.0",
                'session': data['session']
            }
        if data['request']['command'].lower() == 'likwid technologies вездекод':
            response['response'] = {
                "text": "Привет вездекодерам!",
                "tts": "Привет вездекодерам!",
                # "buttons": [
                #   {
                #     "title": "Надпись на кнопке",
                #     "payload": {},
                #     "url": "https://example.com/"
                #   }
                # ],
                "end_session": True
            }
        return Response(response, status.HTTP_200_OK)
