import requests
import accessify


class StarWarsAPI:
    """В далекой-далекой галактике"""
    __url: str = "https://swapi.dev/api/"

    def __init__(self):
        # json ответ
        self.headers ={'content-type': 'application/json'}
        self.response = requests.get(self.url, headers=self.headers).json()
        self.check_status_code(response=self.response)
        # название категории: ссылка
        self.links: dict[str, str] = {i: self.response.get(i) for i in self.response}

    """Служебные методы"""

    @staticmethod
    def check_status_code(response) -> None:
        """Проверка ответа. Если статус-код == 200, то ничего не происходит.
        Иначе поднимается исключение."""
        if response:
            pass
        else:
            raise ConnectionError("Не удалось получить ответ по такому запросу")

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, new_url):
        match input("Вы уверены что хотите сменить url запроса? [Yes/NO]"):
            case "Yes":
                self.__url = new_url
            case _:
                return

    """Методы API ответа"""

    def get_category(self, category: str) -> dict:
        """Получение категории в json формате от API."""
        if not (category in self.links):
            raise ValueError("Неверное название категории")
        else:
            content = requests.get(self.links[category], headers=self.headers).json()
            self.check_status_code(content)
            return content

    def get_fastest_ship(self):
        """Получение самого быстрого космического корабля."""
        ships = self.get_category('starships')['results']
        handled_ships = [{"name": ship['name'], 'speed': ship['max_atmosphering_speed'] } for ship in ships]
        for i in handled_ships:
            if 'km' in i['speed']:
                i['speed'] = int(i['speed'].strip('km'))
            elif i['speed'].isdigit():
                i['speed'] = int(i['speed'])
            elif i['speed'] == 'n/a':
                i['speed'] = 0
            else:
                pass
        max_speed = max((i['speed'] for i in handled_ships))
        for i in handled_ships:
            if i['speed'] == max_speed:
                del ships, handled_ships, max_speed
                return i

    def get_biggest_planet(self):
        """Получение самой большой по диаметру планеты."""
        planets = self.get_category('planets')['results']
        handled_planets = [{"name": planet["name"], "diameter": int(planet["diameter"])} for planet in planets]
        biggest_diameter = max((i['diameter'] for i in handled_planets))

        for planet in handled_planets:
            if planet['diameter'] == biggest_diameter:
                return planet


