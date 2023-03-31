import vk_api
import exceptions
from vk_api.bot_longpoll import VkBotEvent, VkBotLongPoll, VkBotMessageEvent, VkBotEventType


class VKConstants:
    CONTENT_TYPES: tuple = ("text", "photo", "voice", )
    pass


class VKBot(VkBotLongPoll, VKConstants):
    __handler: dict = {"commands": {},
                       "content_types": {}}

    def __init__(self, token, id_):
        try:
            self.__vk_session = vk_api.VkApi(token=token)
            self.__vk = self.__vk_session.get_api()
            super().__init__(self.__vk_session, group_id=id_)
        except vk_api.exceptions.ApiError:
            raise exceptions.VKTokenError

    # объекты свойств
    @property
    def handler(self):
        return self.__handler

    @handler.deleter
    def handler(self):
        raise exceptions.VKDeleteError

    @staticmethod
    def answer_text(text: str,
                    keyboard: dict = None):
        if keyboard is None:
            return {"message": text, }
        else:
            return {"message": text, "keyboard": keyboard}

    @staticmethod
    def answer_image(text: str, peer_id: str, random_id: str,
                     keyboard: dict = None):
        return {"message": text, "peer_id": peer_id, "random_id": random_id,
                "keyboard": keyboard}

    def message_handler(self, commands: list = None, content_types: list = None):
        """Обработчик сообщений"""
        def wrapper(function):
            # если переданы только команды
            if commands and not content_types:
                if all([isinstance(i, str) for i in commands]):
                    for command in commands:
                        self.__handler['commands'][command] = function
                else:
                    raise exceptions.VKBotCommandSetterError

            # если переданы только типы сообщений
            elif content_types and not commands:
                if all([i in self.CONTENT_TYPES for i in content_types]):
                    for content_type in content_types:
                        self.__handler['content_types'][content_type] = function
                else:
                    raise exceptions.VKUnknownContentTypeError
        return wrapper

    def polling(self):
        while True:
            try:
                for event in self.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        message = event.message
                        message_text = message['text']
                        # если сообщение от пользователя
                        if event.from_user:
                            # если это команда
                            if message.text in self.__handler['commands']:

                                self.__vk.messages.send(**self.__handler['commands'][message.text](message),
                                                        random_id=message['random_id'], user_id=message['peer_id'])
                            # если это не команда
                            else:
                                # если существуют обработчики типов
                                if self.__handler['content_types']:
                                    self.__vk.messages.send(**self.__handler['content_types']['text'](message),
                                                        random_id=message['random_id'], user_id=message['peer_id'])

                        # если сообщение в чате
                        elif event.from_chat:
                            pass

                        # если сообщение в группе
                        elif event.from_group:
                            pass
            except:
                raise Exception

