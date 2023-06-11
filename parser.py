import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

URL = {
    'Politico': 'https://www.politico.com/',
    'StopGame': 'https://stopgame.ru/',
    'IGN': 'https://www.ign.com/',
    'Skysports': 'https://www.skysports.com/',
    'Sportguardian': 'https://www.theguardian.com/uk/sport'
}
ua = UserAgent()
headers = {'User-Agent': ua.chrome}


def parse_politico() -> list:
    request = requests.get(URL.get('Politico')).text
    soup = BeautifulSoup(request, 'lxml')

    links = tuple(elem.get('href') for elem in soup.findAll('a',
                                                            class_='js-tealium-tracking'))
    articles = tuple(elem.text for elem in soup.findAll('a',
                                                        class_='js-tealium-tracking'))
    return [_ for _ in zip(articles, links)]


def parse_stopgame() -> list:
    request = requests.get(URL.get('StopGame')).text
    soup = BeautifulSoup(request, 'lxml')

    links = tuple("https://stopgame.ru/" + elem.get('href') for elem in soup.findAll('a',
                                                                                     class_='_news-widget__item_p8g9a_272'))
    articles = tuple(elem.text.replace('\n', '').strip() for elem in soup.findAll('a',
                                                                                  class_='_news-widget__item_p8g9a_272'))
    return [_ for _ in zip(articles, links)]


def parse_ign() -> list:
    request = requests.get(URL.get('IGN'), headers=headers).text
    soup = BeautifulSoup(request, 'lxml')

    links = tuple(elem.get('src') for elem in soup.findAll('img',
                                                           class_='jsx-2920405963 progressive-image jsx-1049729975 item-image aspect-ratio aspect-ratio-16-9 jsx-1330092051 jsx-3166191823 rounded hover-opacity'))
    articles = tuple(elem.get('alt') for elem in soup.findAll('img',
                                                              class_='jsx-2920405963 progressive-image jsx-1049729975 item-image aspect-ratio aspect-ratio-16-9 jsx-1330092051 jsx-3166191823 rounded hover-opacity'))
    return [_ for _ in zip(articles, links)]


def parse_guardiansport():
    request = requests.get(URL.get('Sportguardian')).text
    soup = BeautifulSoup(request, 'lxml')

    articles = tuple(elem.text for elem in soup.findAll('a', class_='u-faux-block-link__overlay js-headline-text'))
    links = tuple(elem.get('href') for elem in soup.findAll('a', class_='u-faux-block-link__overlay js-headline-text'))

    return [_ for _ in zip(articles, links)]


def parse_skysports() -> list:
    request = requests.get(URL.get('Skysports')).text
    soup = BeautifulSoup(request, 'lxml')

    links = tuple(elem.get('href') for elem in soup.findAll('a', class_='sdc-site-tile__headline-link'))
    articles = tuple(elem.text for elem in soup.findAll('span', class_='sdc-site-tile__headline-text'))
    sport_names = tuple(elem.text.strip() for elem in soup.findAll('a', class_='sdc-site-tile__tag-link'))

    return [_ for _ in zip(sport_names, articles, links)]
