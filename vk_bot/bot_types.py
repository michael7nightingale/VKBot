# import vk_api
import json
import exceptions


class KeyboardButton:
    """Класс кнопки для клавиатуры"""
    def __init__(self, text: str, color: str = 'positive'):
        if all((isinstance(i, str) for i in (text, color))):
            self.__button = {
                'action': {
                    "type": "text",
                    "payload": "{\"button\": \"1\" }",
                    "label": text
                },
                "color": color
            }

    @property
    def button(self):
        return self.__button


class ReplyKeyboardMarkup:
    """Класс клавиатуры"""
    keyboard: dict = dict()

    def __init__(self, one_time: bool = True):
        if not isinstance(one_time, bool):
            raise exceptions.VKKeyboardTypeError
        # если все данные определены корректно
        self.__keyboard = {
            "one_time": one_time,
            "buttons": []
        }

    def add(self, button: KeyboardButton) -> None:
        """Добавление кнопки на клавиатуру"""
        if not isinstance(button, KeyboardButton):
            raise exceptions.VKKeyboardTypeError
        else:
            self.__keyboard['buttons'].append([button.button])

    def json_to_str(self) -> str:
        """Возвращает строковое представление json-разметки клавиатуры"""
        return str(
            json.dumps(self.__keyboard, ensure_ascii=False).encode('utf-8').decode('utf-8')
        )
