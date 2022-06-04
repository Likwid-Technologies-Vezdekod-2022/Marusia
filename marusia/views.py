from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


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
        if data['request']['command'].lower() == 'likwid technologies вездекод':
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
        if data['request']['command'] == 'помогите':
            response['response'] = {
                'text': 'Список команд:\nпамагите: Список команд\nlikwid technologies '
                        'вездекод: Привет вездекодерам!\nОпросник: Список последовательно задаваемых вопросов\n\n '
                        'Команды работают с любым регистром',
                'end_session': True,
                'tts': 'Список команд выведен'
            }
        return Response(response, status.HTTP_200_OK)
