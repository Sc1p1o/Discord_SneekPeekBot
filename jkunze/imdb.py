"""
This module is originally written by @jkunze in his own repository for another Discord Bot.
"""
import requests
from bs4 import BeautifulSoup


def get_imdb_link(name, year=""):
    year = str(year)
    url = f"https://www.imdb.com/find/?q={name} {year}&s=tt&ttype=ft&ref_=fn_ft"

    # Quelltext herunterladen
    hdr = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=hdr)
    html_content = response.text

    # BeautifulSoup verwenden, um den Quelltext zu analysieren und die Informationen zu extrahieren
    soup = BeautifulSoup(html_content, "html.parser")

    title_link = soup.find('a', class_='ipc-metadata-list-summary-item__t')
    href = title_link['href']

    link ="https://www.imdb.com" + href
    link = link.split("/?ref_=fn_tt_tt_1")[0]

    return link


def get_rating(imdb_link: str):
    # Quelltext herunterladen
    hdr = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(imdb_link, headers=hdr)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    rating_element = soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})

    # Bewertung extrahieren
    rating = rating_element.text.strip().split('/')[0]
    if rating is None:
        rating = 'NA'
    else:
        rating = rating_element.text.strip().split('/')[0]

    return rating


def get_image(imdb_link: str):
    # Quelltext herunterladen
    hdr = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(imdb_link, headers=hdr)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    image_element = soup.find('div', class_='ipc-poster').find('img', class_='ipc-image')['srcset'].split(', ')[-1].split(' ')[-2]

    return image_element
