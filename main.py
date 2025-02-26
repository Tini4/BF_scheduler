import pickle
import re
from argparse import ArgumentParser, Namespace
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from requests import Session

CACHE_FILE: str = 'cache.pkl'
SCHEDULE_URL: str = 'https://urniki.bf.uni-lj.si'
# SUBJECTS: dict[str, str] = {
#     'BIUN-1': '53', 'BIUN-2': '54', 'BIUN-3': '55',
#     'BTUN-1': '50', 'BTUN-2': '51', 'BTUN-3': '52',
#     'GOUN-1': '47', 'GOUN-2': '48', 'GOUN-3': '49',
#     'AGUN-1': '44', 'AGUN-2': '45', 'AGUN-3': '46',
#     'ZOUN-1': '41', 'ZOUN-2': '42', 'ZOUN-3': '43',
# }


def load_cache() -> dict[str, BeautifulSoup]:
    # noinspection PyBroadException
    try:
        with open(CACHE_FILE, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return {}


def store_cache(cache: dict[str, BeautifulSoup]) -> None:
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache, f)


def get_url(program: str) -> str:
    soup = get_soup_url(SCHEDULE_URL)

    id_ = None
    for div in soup.find_all('div', class_='collapsible-body'):
        for a in div.find_all('a'):
            if a.text == program:
                id_ = urlparse(a.get('href')).path

                break

        if id_ is not None:
            break

    if id_ is None:
        raise RuntimeError(f'Could not find id for {program}')

    return SCHEDULE_URL + id_


def get_query(day: str) -> str:
    if day is None:
        return ''

    return f'?day={day}'


def get_soup_url(url: str, use_cache: bool = True) -> BeautifulSoup:
    cache = load_cache()

    if use_cache and url in cache:
        print(f'cached: {urlparse(url).path} ({url})\n')
    else:
        print(f'retrieving: {urlparse(url).path} ({url})\n')

        session = Session()
        page = session.get(url)
        cache[url] = BeautifulSoup(page.content, 'html.parser')  # 'html5lib')

        store_cache(cache)

    return cache[url]


def get_soup_file(file: str) -> BeautifulSoup:
    with open(file, 'r', encoding='utf-8') as _f:
        return BeautifulSoup(_f.read(), 'html.parser')  # 'html5lib')


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        prog='FRI_scheduler',
        description='Create your schedule for FRI faculty.',
        epilog='by Tini4'
    )
    parser.add_argument('program',
                        help='Program and year (e.g. BTUN-1)')
    parser.add_argument('-d', '--date',
                        help='Schedule date (e.g. 2025-03-03)')
    parser.add_argument('-c', '--cache', action='store_false',
                        help='Disable caching')

    args = parser.parse_args()

    return args


def main() -> None:
    args = parse_arguments()

    soup = get_soup_url(get_url(args.program) + get_query(args.date), args.cache)

    with open('original.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    # Add main.js
    soup.head.append(soup.new_tag('script', src='static/main.js'))

    # Add style.css
    soup.head.append(soup.new_tag('link', href='static/style.css', rel='stylesheet'))

    # Disable links
    for a in soup.find_all('a'):
        a.attrs.pop('href', None)

    # Remove groups
    for div in soup.find_all('span', class_='layer_one'):
        div.decompose()

    # Recolour
    for div in soup.find_all('div', class_='entry'):
        div['style'] = re.sub(r'(hsla\(.+, .+%, ).+(%, .+\))', r'\g<1>35\g<2>', div['style'])

    with open('modified.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    print(Path('modified.html').absolute().as_uri())


if __name__ == '__main__':
    main()
