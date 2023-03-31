from vk_bot import vk_bot
from vk_bot import bot_types
import API.starwars


"""https://vk.com/guitar_music_all"""

token = "vk1.a.iQocA6-CTdKBTOQ86dijbvdjSB0J_JH2Ep6qEhXHcrv0Hab8ZRP3pRrbbt0KcxbPGV06mhZ-HiuOXScWD6FUirFQgwTAcZqZhJD7bPmEG2BLrm2mvkl8Qz0mP2cANhux26l2ftqooUFaObjvtgYPadUe87LPnzgzCRrN270FImb-q3PenE0Ywnsp_tYN6Zp2vBh3iEZtrDIaExZ_1kXwXQ"
id_ = "178712947"   # id сообщества
bot = vk_bot.VKBot(token, id_)
star_api = API.starwars.StarWarsAPI()


"""На 2 модуле мы с вами писали парсер звёздных войн. Внедрите парсер в нашего с вами бота. 
Добавьте отклик на сообщение с текстом “планеты”. 
При вводе такого текста сообщения бот должен выдавать планету с максимальным диаметром. 
Ссылка на API -> https://swapi.dev/api/"""

"""Добавьте ещё один парсер. Добавьте отклик на сообщение пользователя: “корабли”. 
При вводе такого текста сообщения бот должен выдавать звёздный корабль с максимальной скоростью. 
Ссылка на API -> https://swapi.dev/api/"""


@bot.message_handler(commands=['Привет', 'привет', 'прив'])
def hello(message):
    keyboard = bot_types.ReplyKeyboardMarkup(one_time=False)
    button1 = bot_types.KeyboardButton(text='корабли')
    button2 = bot_types.KeyboardButton(text='планеты')
    keyboard.add(button1)
    keyboard.add(button2)
    return bot.answer_text(text='Привет, давай начнём работать', keyboard=keyboard.json_to_str())


@bot.message_handler(commands=['корабли', ])
def send_ships(message):
    fastest_ship = star_api.get_fastest_ship()
    return bot.answer_text(text="""Самый быстрый корабль - {}.
                            Его максимальная скорость составляет {} км/час""".format(*fastest_ship.values()))


@bot.message_handler(commands=['планеты'])
def send_planets(message):
    biggest_planet = star_api.get_biggest_planet()
    return bot.answer_text(text="""Самая большая планета - {}.
                                Её диаметр составляет {} км.""".format(*biggest_planet.values()))


@bot.message_handler(content_types=['text'])
def common_text(message):
    return bot.answer_text(text='Your text: \'{}\''.format(message['text']))


if __name__ == '__main__':
    bot.polling()
