"""
This module is originally written by @jkunze in his own repository for another Discord Bot. 'Chance' as an additional
returned value is added by me for my own needs.
"""

import requests
from bs4 import BeautifulSoup
from jkunze import imdb


def scrape_sneak():
    # URL der Seite
    url = "http://5.45.100.152/sneakprognose.php?SPO=Leipzig&SPK=Cinestar&SPN=Sneak+Preview"

    # Quelltext herunterladen
    response = requests.get(url)
    html_content = response.text

    # BeautifulSoup verwenden, um den Quelltext zu analysieren und die Informationen zu extrahieren
    soup = BeautifulSoup(html_content, "html.parser")

    # Liste zur Speicherung der extrahierten Informationen
    movies = []
    test = soup.find_all("tr", class_="lvct2")
    # Durch die Tabellenzeilen iterieren und Informationen extrahieren
    for row in soup.find_all("tr", class_="lvct2")[:10]:
        columns = row.find_all("td")

        title = columns[3].a.text.strip()
        genre_and_year = columns[3].text.split(title)[1]
        genre_and_year = genre_and_year.split("von")[0].strip()
        year, genre = genre_and_year[:4], genre_and_year[5:]

        genre = ", ".join(genre.split(' / '))

        chance = columns[1].contents[0].attrs.get('style')

        chance_width = 0
        parts = chance.split(";")  # Teilt den String an jedem Semikolon
        for part in parts:
            if 'width' in part:  # Findet den Teil mit 'width'
                chance_width = (int(part.split(":")[1]) / 106) * 100
                break

        imdb_link = imdb.get_imdb_link(title, year)
        rating = imdb.get_rating(imdb_link)

        movie = {
            "Rank": columns[0].text.strip(),
            "Title": title,
            "Genre": genre,
            "Year": year,
            "Chance": round(chance_width, 2),
            #"IMDB": imdb_link,
            #"Cover": image_link,
            "IMDB": rating
        }
        movies.append(movie)

    return movies
