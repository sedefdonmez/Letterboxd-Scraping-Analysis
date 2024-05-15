import requests
from bs4 import BeautifulSoup

# Hedef URL
url = 'https://letterboxd.com/films/popular/this/week/decade/2020s/'

# HTTP isteğini yap
response = requests.get(url)

# Eğer istek başarılıysa içeriği parse et
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Filmlerin listelendiği her bir öğeyi bul
    films = soup.select('li.listitem.poster-container.film-not-watched')  # Güncellenmiş seçici

    for film in films:
        name = film.select_one('div.react-component[data-film-name]').get('data-film-name') if film.select_one('div.react-component[data-film-name]') else 'No title available'
        year = film.select_one('div.react-component[data-film-release-year]').get('data-film-release-year') if film.select_one('div.react-component[data-film-release-year]') else 'Year not available'
        image = film.select_one('img').get('src') if film.select_one('img') else 'No image available'

        print(f"Film Name: {name}, Year: {year}, Image: {image}")

else:
    print("Failed to retrieve the page")
