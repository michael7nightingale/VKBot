class VKError(Exception):
    message: str
    """Базовая ошибка сервисов ВК"""
    # def __init__(self):
    #     print(self.message)
    def __repr__(self):
        return self.message


class VKTokenError(VKError):
    message = """Ошибка токена"""


class VKNoNewMessagesError(VKError):
    message = """Отсутствуют новые сообщения"""


class VKDeleteError(VKError):
    message = """Запрещено грубое удаление конфигураций"""


class VKBotCommandSetterError(VKError):
    message = """Некорректная команда"""


class VKUnknownContentTypeError(VKError):
    message = """Некорректная команда"""


class VKKeyboardTypeError(VKError):
    message = """Некорректный тип аттрибута клавиатуры"""


