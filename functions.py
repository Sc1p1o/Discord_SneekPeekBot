import re

def ist_noob(text: str):
    n_pattern = r'n{1,}'
    o_pattern = r'o{1,}'
    b_pattern = r'b{1,}'

    return bool(re.search(n_pattern, text, re.IGNORECASE) and re.search(o_pattern, text, re.IGNORECASE) and
                re.search(b_pattern, text, re.IGNORECASE))


def get_movie_info(text: str):
    trailer_url: str = 'test_url.test'
    rating: float = 6.9

    return {'imdb_rating': rating, 'trailer_url': trailer_url}
