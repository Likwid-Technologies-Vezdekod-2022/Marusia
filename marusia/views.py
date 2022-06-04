from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from fuzzywuzzy import fuzz

QUESTIONS = [
    {
        'question': 'Что такое http 404',
        'answers': [
            ('Кто я?', False),
            ('Ошибка говорящая, что сервер не доступен', False),
            ('Шуточная ошибка, в оригинале звучащая как You are teapot, в переводе: ты чайник', False),
            ('Страница не найдена', True),
        ]
    },
    {
        'question': 'Как в питоне разделить строку',
        'answers': [
            ('На ноль конечно', False),
            ('Использовать встроенноую фукнцию split', False),
            ('Использовать строковый метод split', True),
            ('Использовать строковый метод div', False),
        ]
    },
    {
        'question': 'Какой линукс чаще всего используется для работы в области системной безопасности?',
        'answers': [
            ('Windows 95', False),
            ('kali', True),
            ('ubuntu', False),
            ('Arch', False),
        ]
    },
    {
        'question': 'Открыто ли api у телеграма?',
        'answers': [
            ('Кто такой api?', False),
            ('Да', True),
            ('Нет', False),
        ]
    },
    {
        'question': 'Что на js выдаст программа: \'2\'+\'2\'-\'2\'',
        'answers': [
            ('Исключение', False),
            ('2', False),
            ('20', True),
            ('-infinity', False),
        ]
    },
    {
        'question': 'Что такое XR',
        'answers': [
            ('Второе название для HR', False),
            ('Дополненая реальность', True),
            ('Нееронные сети', False),
            ('Мобильная разработка', False),
        ]
    },
    {
        'question': 'Самый популярный язык для мобильной разработки в 2007',
        'answers': [
            ('Python 3.10', False),
            ('Kotlin', False),
            ('Java', True),
            ('Unity', False),
        ]
    },
    {
        'question': 'На каком голосовом помошнике ты проходишь этот квиз?',
        'answers': [
            ('Джарвис', False),
            ('Алиса', False),
            ('Гоша Дударь', False),
            ('Маруся', True),
        ]
    },
]


class MarusiaCommandsView(APIView):
    def get_answers(self, question):
        text = ''
        counter = 0
        for answer in QUESTIONS[question]['answers']:
            counter += 1
            text += f'{counter}) {answer[0]} \n\n'
        return text

    def _help(self):
        self.response['response'] = {
                'text': 'Список команд:\nпамагите: Список команд\nlikwid technologies '
                        'вездекод: Привет вездекодерам!\nОпросник: Список последовательно задаваемых вопросов\n\n '
                        'Команды работают с любым регистром',
                'end_session': True,
                'tts': 'Список команд выведен'
            }

        return self.response

    def _hello(self):
        self.response['response'] = {
            'text': 'Привет вездекодерам!',
            'tts': 'Привет вездекодерам!',
            'end_session': True
        }
        return self.response

    def _quiz_start(self):
        self.response['response'] = {
            'text': QUESTIONS[0]['question'] + '\n\n',
            'end_session': False,
            'tts': f"<?xml version =\"1.0\" encoding=\"UTF-8\"?><speak version=\"1.1\" xmlns:mailru=\"["
                   f"http://vc.go.mail.ru]\" lang=\"ru\"><s>{QUESTIONS[0]['question']}</s><break time=\"1.00s\"/>"
                   f"<speaker audio=\"marusia-sounds/things-bell-1\"/>",
            "card": {
                "type": "BigImage",
                "image_id": 457239018
            },
        }
        self.response['response']['text'] += self.get_answers(0)
        self.response['session_state']['prev_question'] = 0
        self.response['session_state']['result_counter'] = 0
        return self.response

    def _quiz(self, data):
        try:
            answer = int(data['request']['command'])
        except:
            text = 'ты видимо не справился с кнопкой, попробуй ещё раз, вводить надо цифры'
            tts = text
            self.response['response'] = {
                'tts': tts,
                'text': text,
                'end_session': False,
            }
            self.response['session_state'] = self.state
            return self.response
        answers = QUESTIONS[self.state['prev_question']]['answers']
        if 1 <= answer <= len(answers):
            if answers[answer - 1][1]:
                text = 'Правельный ответ!'
                self.state['result_counter'] += 1
            else:
                text = 'Неправельно'
            try:
                text += '\n\n' + QUESTIONS[self.state['prev_question'] + 1]['question']
                tts = text
                text += ' \n\n' + self.get_answers(self.state['prev_question'] + 1)
            except:
                pass
            self.state['prev_question'] += 1
        else:
            text = f'ты видимо не справился с кнопкой, попробуй ещё раз \n\n'
            tts = text
            text += self.get_answers(self.state['prev_question'])
        if self.state['prev_question'] < 8:
            self.response['response'] = {
                'tts': tts + '<break time=\"1.00s\"/><speaker audio=\"marusia-sounds/things-bell-1\"/>',
                'text': text,
                'end_session': False,
            }
            self.response['session_state'] = self.state
        else:
            if self.state["result_counter"] == 1:
                ending = 'о'
            elif 5 > self.state["result_counter"] > 1:
                ending = 'а'
            else:
                ending = 'ов'
            text = f'Квиз завершён, вы набрали {self.state["result_counter"]} очк' + ending + '\n\n'
            if self.state["result_counter"] >= 4:
                text += 'Вы правельно ответили на большую чать вопросов, соответственно вы знакомы с большей ' \
                        'частью котегорий, рекомендуем вам поучаствовать во всех '
            else:
                text += 'Вы не справились с большенством вопросов, рекомендоуем вам по больше учиться и ' \
                        'выберать те котегории, в которых вы чуствуете себя уверенно '
            self.response['response'] = {
                'tts': text + '<break time=\"1.00s\"/><speaker audio=\"marusia-sounds/things-bell-1\"/>',
                'text': text,
                'end_session': True,
                "commands": [
                    {
                        "type": "MiniApp",
                        "url": ["https://vk.com/app7543093"]
                    },
                    # {
                    #     "type": "BigImage",
                    #     "image_id": 457239019
                    # }
                ],
            }
        return self.response

    def post(self, request):
        data = request.data
        self.state = data['state']['session']
        self.response = {
            'response': {
                'text': 'Неизвестная команда\nСписок команд:\nпомогите: Список команд\nlikwid technologies '
                        'вездекод: Привет вездекодерам!\nОпросник: Список последовательно задаваемых вопросов\n\n '
                        'Команды работают с любым регистром',
                'tts': 'неизвестная команда',
                'end_session': True
            },
            'version': '1.0',
            'session': data['session'],
            'session_state': {}
        }
        response = self.response
        if fuzz.ratio(data['request']['command'].lower(), 'likwid technologies вездекод') > 70:
            response = self._hello()
        if fuzz.ratio(data['request']['command'].lower(), 'помогите') > 70:
            response = self._help()
        if fuzz.ratio(data['request']['command'].lower(), 'викторина') > 70:
            response = self._quiz_start()
        if 'prev_question' in self.state:
            response = self._quiz(data)

        return Response(response, status.HTTP_200_OK)
