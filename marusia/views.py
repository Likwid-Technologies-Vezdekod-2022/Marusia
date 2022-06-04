from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from fuzzywuzzy import fuzz


class MarusiaCommandsView(APIView):
    def post(self, request):
        data = request.data
        response = {
            'response': {
                'text': 'Неизвестная команда\nСписок команд:\nпомогите: Список команд\nlikwid technologies '
                        'вездекод: Привет вездекодерам!\nОпросник: Список последовательно задаваемых вопросов\n\n '
                        'Команды работают с любым регистром',
                'tts': 'неизвестная команда',
                'end_session': True
            },
            'version': '1.0',
            'session': data['session']
        }
        if fuzz.ratio(data['request']['command'].lower(), 'likwid technologies вездеход') > 70:
            response['response'] = {
                'text': 'Привет вездекодерам!',
                'tts': 'Привет вездекодерам!',
                # 'buttons': [
                #   {
                #     'title': 'Надпись на кнопке',
                #     'payload': {},
                #     'url': 'https://example.com/'
                #   }
                # ],
                'end_session': True
            }
        if fuzz.ratio(data['request']['command'], 'помогите') > 70:
            response['response'] = {
                'text': 'Список команд:\nпамагите: Список команд\nlikwid technologies '
                        'вездекод: Привет вездекодерам!\nОпросник: Список последовательно задаваемых вопросов\n\n '
                        'Команды работают с любым регистром',
                'end_session': True,
                'tts': 'Список команд выведен'
            }
        if fuzz.ratio(data['request']['command'], 'Опросник') > 70:
            response['response'] = {
                'text': 'indev',
                'end_session': True,
                'tts': 'in dev'
            }
        return Response(response, status.HTTP_200_OK)
