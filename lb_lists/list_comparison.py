from google.colab import drive
import requests
from bs4 import BeautifulSoup
import time


def conn_to_drive(remount:bool = False):
    drive.mount("/content/gdrive/", force_remount=remount)


def get_watchlist(author:str, folder, title:str="Watchlist"):
  watchlist_url = 'https://letterboxd.com/' + author + '/watchlist'
  title = title + ' | ' + author
  movies = get_movies_v2(watchlist_url)
  with open("gdrive/MyDrive/Letterboxd/" + title + ".txt", 'w+') as f:
    for m in movies:
      f.write(m + '\n')
  return movies


def get_watched(author:str, folder, title:str="Watched", print_links=False):
  watched_url = 'https://letterboxd.com/' + author + '/films'
  title = f'{title} | {author}'

  movies = get_movies_v2(watched_url, print_links)

  with open(f"gdrive/MyDrive/{folder}/{title}.txt", 'w') as f:
    for m in movies:
      f.write(m+'\n')
  return movies


def get_html(url):
  soup = requests.get(url)
  return BeautifulSoup(soup.content, 'html.parser')


def get_last_page(soup):
  check = soup.find("li", class_="paginate-page")
  if check:
    return int(soup.find_all("li", class_="paginate-page")[-1].getText())
  return 1


def get_title_and_year(link:str):
  movie_page = get_html(link)
  title_year = str(movie_page.find("meta", property="og:title")["content"])
  if "(" in title_year:
    title = title_year.split("(")[0][:-1]
    year = title_year.split("(")[1][:-1]
  else:
    title = title_year
    year = ""
  return f'{title}, {year}'


def get_movies_v2(url:str, print_links=False, range_:tuple=None):
  soup = get_html(url)
  movies = []
  end = False
  last_page = get_last_page(soup)

  if range_:
    first, last = range_
    last += 1
    if last > last_page:
      last = last_page
  else:
    first, last = 1, last_page+1

  for p in range(first, last):
    print(f'page {str(p)}/{str(last_page)}')
    page_url = f'{url}/page/{str(p)}'
    soup = get_html(page_url)
    soup = soup.find_all("div", class_="poster")
    soup = str(soup).split(' ')
    soup = [s for s in soup if 'data-target-link=' in s]

    for movie in soup:
      time.sleep(1)
      link = movie[24:-1]
      movie_link = f'https://letterboxd.com/film/{link}'
      if print_links:
        print(f"   {str(movie_link)}")
      title_year = get_title_and_year(movie_link)
      movies.append(f'{title_year}')
  return movies
