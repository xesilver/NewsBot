import asyncio
import aiohttp
import db
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time

URL = {
    'politico': 'https://www.politico.com/',
    'stopgame': 'https://stopgame.ru/news',
    'thegamer': 'https://www.thegamer.com/category/game-news/',
    'skysports': 'https://www.skysports.com/',
    'sportguardian': 'https://www.theguardian.com/uk/sport',
    'voanews': 'https://www.voanews.com/',
    'cnn': 'https://edition.cnn.com/politics',
    'gamespot': 'https://www.gamespot.com/',
    'euronews': 'https://www.euronews.com/news/international',
    'bbc': 'https://www.bbc.com/news',
    'rt': 'https://www.rt.com/',
    'xfire': 'https://www.xfire.com/news/',
    'playground': 'https://www.playground.ru/news',
    'kotaku': 'https://kotaku.com/culture/news',
    'vg247': 'https://www.vg247.com/',
    'sportingnews': 'https://www.sportingnews.com/us',
    'deadspin': 'https://deadspin.com/',
    'euronews_sport': 'https://www.euronews.com/news/sport',
    'cnn_sport': 'https://edition.cnn.com/sport',
}

headers = {'User-Agent': UserAgent().chrome}


async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    '''
    This function makes a request to url page you provide in variable `url` and returns the html page.

        Parameters:
        session (aiohttp.ClientSession): The client session to use for making the request.
        url (str): The link of the web-page which will be parsed.

        Returns:
        str: The response data as a string.
    '''

    async with session.get(url, headers=headers) as response:
        return await response.text()


# Block of code responding for the requests on different news portals.
async def parse_politico() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('politico'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple(elem.get('href') for elem in
                      soup.find('ol', class_='media-item-list media-item-list--timestamps').findAll('a',
                                                                                                    class_='js-tealium-tracking'))
        articles = tuple(elem.text for elem in
                         soup.find('ol', class_='media-item-list media-item-list--timestamps').findAll('a',
                                                                                                       class_='js-tealium-tracking'))

        return 'politico', [_ for _ in zip(articles, links)]


async def parse_voanews() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('voanews'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple('https://www.voanews.com/' + elem.get('href') for elem in
                      soup.findAll('a', class_='img-wrap img-wrap--t-spac img-wrap--size-4 img-wrap--float'))
        articles = tuple(elem.text.replace('\n', '').strip() for elem in
                         soup.findAll('h4', class_='media-block__title media-block__title--size-4'))

        return 'voanews', [_ for _ in zip(articles, links)]


async def parse_stopgame() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('stopgame'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple(
            'https://stopgame.ru/' + elem.get('href') for elem in soup.find('div', class_='list-view').findAll('a',
                                                                                                               class_='_title_1tbpr_49'))
        articles = tuple(
            elem.text.replace('\n', '').strip() for elem in soup.find('div', class_='list-view').findAll('a',
                                                                                                         class_='_title_1tbpr_49'))

        return 'stopgame', [_ for _ in zip(articles, links)]


async def parse_thegamer() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('thegamer'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple('https://www.thegamer.com/' + elem.get('href') for elem in
                      soup.find('div', class_='sentinel-listing-page-list').findAll('a',
                                                                                    class_='dc-img-link'))
        articles = tuple(elem.text.replace('\n', '').strip() for elem in
                         soup.find('div', class_='sentinel-listing-page-list').findAll('h5',
                                                                                       class_='display-card-title'))

        return 'thegamer', [_ for _ in zip(articles, links)]


async def parse_guardiansport() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('sportguardian'))
        soup = BeautifulSoup(html, 'lxml')

        articles = tuple(elem.text for elem in soup.findAll('a', class_='u-faux-block-link__overlay js-headline-text'))
        links = tuple(
            elem.get('href') for elem in soup.findAll('a', class_='u-faux-block-link__overlay js-headline-text'))

        return 'guardiansport', [_ for _ in zip(articles, links)]


async def parse_skysports() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('skysports'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple('https://www.skysports.com/' + elem.get('href') for elem in
                      soup.findAll('a', class_='sdc-site-tile__headline-link'))
        articles = tuple(elem.text for elem in soup.findAll('span', class_='sdc-site-tile__headline-text'))

        return 'skysports', [_ for _ in zip(articles, links)]


async def parse_gamespot() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('gamespot'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple(elem.get('src') for elem in soup.find('section',
                                                            class_='promo-strip promo-strip--grid promo-strip--grid--quarter span12').findAll(
            'img'))
        articles = tuple(elem.text for elem in soup.find('section',
                                                         class_='promo-strip promo-strip--grid promo-strip--grid--quarter span12').findAll(
            'h3'))

        return 'gamespot', [_ for _ in zip(articles, links)]


async def parse_cnn() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('cnn'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple('https://edition.cnn.com/' + elem.get('href') for elem in
                      soup.find('div', class_='zone__items layout--wide-left-balanced-2').findAll('a',
                                                                                                  class_='container__link container_lead-plus-headlines__link'))
        articles = tuple(elem.text.replace('\n', '').strip() for elem in
                         soup.find('div', class_='zone__items layout--wide-left-balanced-2').findAll('a',
                                                                                                     class_='container__link container_lead-plus-headlines__link'))

        return 'cnn', [_ for _ in zip(articles, links)]


async def parse_bbc() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('bbc'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple('https://www.bbc.com/' + elem.get('href') for elem in
                      soup.find('div', class_='gel-wrap gs-u-pt+').findAll('a',
                                                                           class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor'))
        articles = tuple(elem.text for elem in soup.find('div', class_='gel-wrap gs-u-pt+').findAll('h3',
                                                                                                    class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text'))

        return 'bbc', [_ for _ in zip(articles, links)]


async def parse_euronews() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('euronews'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple('https://www.euronews.com/' + elem.get('href') for elem in
                      soup.find('div', class_='o-block-more-news-themes__main').findAll('a',
                                                                                        class_='m-object__title__link'))

        articles = tuple(elem.get('title').replace('\n', '').strip() for elem in
                         soup.find('div', class_='o-block-more-news-themes__main').findAll('a',
                                                                                           class_='m-object__title__link'))

        return 'euronews', [_ for _ in zip(articles, links)]


async def parse_rt() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('rt'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple('https://www.rt.com/' + elem.get('href') for elem in
                      soup.find('div', class_='main-promobox').findAll('a', class_='main-promobox__heading'))
        articles = tuple(elem.text.replace('\n', '').strip() for elem in
                         soup.find('div', class_='main-promobox').findAll('span', class_='main-promobox__link'))

        return 'rt', [_ for _ in zip(articles, links)]


async def parse_xfire() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('xfire'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple(elem.get('href') for elem in
                      soup.find('div',
                                class_='bb-post-collection hfeed post-list list list big-item bb-thumbnail-stretched').findAll(
                          'a', rel='bookmark'))

        articles = tuple(elem.text.replace('\n', '').strip() for elem in
                         soup.find('div',
                                   class_='bb-post-collection hfeed post-list list list big-item bb-thumbnail-stretched').findAll(
                             'a', rel='bookmark'))

        return 'xfire', [_ for _ in zip(articles, links)]


async def parse_kotaku() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('kotaku'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple(elem.get('href') for elem in
                      soup.find('div', class_='sc-17uq8ex-0 fakHlO').findAll('a',
                                                                             class_='sc-1out364-0 dPMosf js_link') if
                      'http' in elem.get('href'))
        articles = tuple(elem.text.replace('\n', '').strip() for elem in
                         soup.find('div', class_='sc-17uq8ex-0 fakHlO').findAll('h2',
                                                                                class_='sc-759qgu-0 kygHWE sc-cw4lnv-6 kTWlYS'))

        return 'kotaku', [_ for _ in zip(articles, links)]


async def parse_vg247() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('vg247'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple(elem.get('href') for elem in
                      soup.find('section', class_='shelf').findAll('a', class_='link_overlay'))
        articles = tuple(elem.get('title').replace('\n', '').strip() for elem in
                         soup.find('section', class_='shelf').findAll('a', class_='link_overlay'))

        return 'vg247', [_ for _ in zip(articles, links)]


async def parse_sportingnews() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('sportingnews'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple('https://www.sportingnews.com/us' + elem.get('href') for elem in
                      soup.find('div', class_='latest-news-sidebar').findAll('a'))

        articles = tuple(elem.text.replace('\n', '').strip() for elem in
                         soup.find('div', class_='latest-news-sidebar').findAll('a'))

        return 'sportingnews', [_ for _ in zip(articles, links)]


async def parse_deadspin() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('deadspin'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple(elem.get('href') for elem in
                      soup.find('div', class_='sc-1w4b9xk-0 ffAumw').findAll('a',
                                                                             class_='sc-1out364-0 dPMosf sc-1pw4fyi-5 hkpnLX js_link'))
        articles = tuple(elem.text.replace('\n', '').strip() for elem in
                         soup.find('div', class_='sc-1w4b9xk-0 ffAumw').findAll('h4', class_='sc-1qoge05-0 nvHxA'))

        return 'deadspin', [_ for _ in zip(articles, links)]


async def parse_cnn_sport() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('cnn_sport'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple(elem.get('href') for elem in
                      soup.find('div', class_='zone__items layout--wide-left-balanced-2').findAll('a',
                                                                                                  'container__link container_lead-plus-headlines-with-images__link container_lead-plus-headlines-with-images__left container_lead-plus-headlines-with-images__light'))
        articles = tuple(elem.text.replace('\n', '').strip() for elem in
                         soup.find('div', class_='zone__items layout--wide-left-balanced-2').findAll('span'))

        return 'cnn_sport', [_ for _ in zip(articles, links)]


async def parse_euronews_sport() -> tuple:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL.get('euronews_sport'))
        soup = BeautifulSoup(html, 'lxml')

        links = tuple('https://www.euronews.com/' + elem.get('href') for elem in
                      soup.find('div', class_='o-block-more-news-themes__main').findAll('a',
                                                                                        class_='m-object__title__link'))

        articles = tuple(elem.get('title').replace('\n', '').strip() for elem in
                         soup.find('div', class_='o-block-more-news-themes__main').findAll('a',
                                                                                           class_='m-object__title__link'))

        return 'euronews_sport', [_ for _ in zip(articles, links)]


# Function which performs asynchronous requests on all news portals every 5 minutes.
# All the results are written into database using a `db` module.
async def main() -> None:
    while True:
        start_time = time.time()
        tasks = [
            asyncio.create_task(parse_skysports()),
            asyncio.create_task(parse_guardiansport()),
            asyncio.create_task(parse_thegamer()),
            asyncio.create_task(parse_stopgame()),
            asyncio.create_task(parse_politico()),
            asyncio.create_task(parse_voanews()),
            asyncio.create_task(parse_cnn()),
            asyncio.create_task(parse_bbc()),
            asyncio.create_task(parse_euronews()),
            asyncio.create_task(parse_rt()),
            asyncio.create_task(parse_deadspin()),
            asyncio.create_task(parse_xfire()),
            asyncio.create_task(parse_vg247()),
            asyncio.create_task(parse_sportingnews()),
            asyncio.create_task(parse_kotaku()),
            asyncio.create_task(parse_gamespot()),
            asyncio.create_task(parse_cnn_sport()),
            asyncio.create_task(parse_euronews_sport()),
        ]
        connection = db.DbConnection()
        await connection.create_pool()

        for result in await asyncio.gather(*tasks):
            await connection.update_news(paper_name=result[0], news=result[1])

        print(f'Parsing took {time.time() - start_time} seconds')

        await asyncio.sleep(300)
