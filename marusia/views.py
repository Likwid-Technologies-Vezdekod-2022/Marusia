from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from fuzzywuzzy import fuzz


QUESTIONS = [
    {
        'question': 'Что такое http 404',
        'answers': {
            'Кто я?': False,
            'Ошибка говорящая, что сервер не доступен': False,
            'Шуточная ошибка, в оригинале звучащая как You are teapot, в переводе: ты чайник': False,
            'Страница не найдена': True,
        }
    },
    {
        'question': 'Как в питоне разделить строку',
        'answers': {
            'На ноль конечно': False,
            'Использовать встроенноую фукнцию split': False,
            'Использовать строковый метод split': True,
            'Использовать строковый метод div': False,
        }
    },
    {
        'question': 'Какой линукс чаще всего используется для работы в области систесмной безопасности?',
        'answers': {
            'Windows 95': False,
            'kali': True,
            'ubuntu': False,
            'Arch': False,
        }
    },
    {
        'question': 'Открыто ли api у телеграма?',
        'answers': {
            'Кто такой api?': False,
            'Да': True,
            'Нет': False,
        }
    },
    {
        'question': 'Что на js выдаст программа: \'2\'+\'2\'-\'2\'',
        'answers': {
            'Исключение': False,
            '2': False,
            '20': True,
            '-infinity': False,
        }
    },
    {
        'question': 'Что такое XR',
        'answers': {
            'Второе название для HR': False,
            'Дополненая реальность': True,
            'Нееронные сети': False,
            'Мобильная разработка': False,
        }
    },
    {
        'question': 'Самый популярный язык для мобильной разработки в 2007',
        'answers': {
            'Python 3.10': False,
            'Kotlin': False,
            'Java': True,
            'Unity': False,
        }
    },
    {
        'question': 'На каком голосовом помошнике ты проходишь этот квиз?',
        'answers': {
            'Джарвис': False,
            'Алиса': False,
            'Гоша Дударь': False,
            'Маруся': True,
        }
    },
]


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
                'text': QUESTIONS[0]['question'] + '\n\n',
                'end_session': False,
                'tts': QUESTIONS[0]['question'],
                'buttons': [],
            }
            counter = 0
            for answer in QUESTIONS[0]['answers']:
                counter += 1
                response['response']['text'] += f'{counter}) {answer} \n\n'
        return Response(response, status.HTTP_200_OK)
