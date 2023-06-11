import asyncio
import aiohttp
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time


URL = {
    'politico': 'https://www.politico.com/',
    'stopgame': 'https://stopgame.ru/',
    'ign': 'https://www.ign.com/',
    'skysports': 'https://www.skysports.com/',
    'sportguardian': 'https://www.theguardian.com/uk/sport'
}

headers = {'User-Agent': UserAgent().chrome}


async def fetch(session, url):
    async with session.get(url, headers=headers) as response:
        return await response.text()


async def parse_politico():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('politico'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple(elem.get('href') for elem in soup.findAll('a', class_='js-tealium-tracking'))
        articles = tuple(elem.text for elem in soup.findAll('a', class_='js-tealium-tracking'))

        return [_ for _ in zip(articles, links)]


async def parse_stopgame():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('stopgame'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple("https://stopgame.ru/" + elem.get('href') for elem in soup.findAll('a',
                                                                                         class_='_news-widget__item_p8g9a_272'))
        articles = tuple(elem.text.replace('n', '').strip() for elem in soup.findAll('a',
                                                                                      class_='_news-widget__item_p8g9a_272'))

        return [_ for _ in zip(articles, links)]


async def parse_ign():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('ign'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple(elem.get('src') for elem in soup.findAll('img',
                                                               class_='jsx-2920405963 progressive-image jsx-1049729975 item-image aspect-ratio aspect-ratio-16-9 jsx-1330092051 jsx-3166191823 rounded hover-opacity'))
        articles = tuple(elem.get('alt') for elem in soup.findAll('img',
                                                                  class_='jsx-2920405963 progressive-image jsx-1049729975 item-image aspect-ratio aspect-ratio-16-9 jsx-1330092051 jsx-3166191823 rounded hover-opacity'))

        return [_ for _ in zip(articles, links)]


async def parse_guardiansport():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('sportguardian'))
        soup = BeautifulSoup(html, 'lxml')

        articles = tuple(elem.text for elem in soup.findAll('a', class_='u-faux-block-link__overlay js-headline-text'))
        links = tuple(elem.get('href') for elem in soup.findAll('a', class_='u-faux-block-link__overlay js-headline-text'))

        return [_ for _ in zip(articles, links)]


async def parse_skysports():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('skysports'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple(elem.get('href') for elem in soup.findAll('a', class_='sdc-site-tile__headline-link'))
        articles = tuple(elem.text for elem in soup.findAll('span', class_='sdc-site-tile__headline-text'))
        sport_names = tuple(elem.text.strip() for elem in soup.findAll('a', class_='sdc-site-tile__tag-link'))

        return [_ for _ in zip(sport_names, articles, links)]


async def main():
    start = time.time()
    tasks = [
        asyncio.create_task(parse_skysports()),
        asyncio.create_task(parse_guardiansport()),
        asyncio.create_task(parse_ign()),
        asyncio.create_task(parse_stopgame()),
        asyncio.create_task(parse_politico())
    ]

    for result in await asyncio.gather(*tasks):
        print(result)

    end = time.time()
    total_time = end - start
    print(total_time)

asyncio.run(main())
