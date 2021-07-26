import os
import numpy as np
import random
import re
import time
import requests
from bs4 import BeautifulSoup


def get_last_page(soup):
  check = soup.find("li", class_="paginate-page")
  if check:
    return int(soup.find_all("li", class_="paginate-page")[-1].getText())
  return 1


def get_movies(url:str):
  soup = requests.get(url)
  soup = BeautifulSoup(soup.content, 'html.parser')
  last_page = get_last_page(soup)
  movies = []
  for p in range(1, last_page+1):
    print('page ' + str(p))
    page_url = url+'/page/'+str(p)
    soup = requests.get(page_url)
    soup = BeautifulSoup(soup.content, 'html.parser')
    soup = soup.find_all("div", class_="poster")
    for movie in soup:
      time.sleep(2)
      movie_link = 'https://letterboxd.com' + movie['data-film-slug']
      print("   " + str(movie_link))
      movie_page = requests.get(movie_link)
      movie_page_content = BeautifulSoup(movie_page.content, "html.parser")
      title_year = str(movie_page_content.find("meta", property="og:title")["content"])
      if "(" in title_year:
        title = title_year.split("(")[0][:-1]
        year = title_year.split("(")[1][:-1]
      else:
        title = title_year
        year = ""
      movies.append(title + ", " + year)
  return movies


def read_from_file(file_name:str):
  with open("../lists/" + file_name + '.txt' , "r") as f:
          movies = f.read().split('\n')
  return movies


def get_actor_movies(actor:str, reload:bool=False):
  movies = []
  if reload:
    actor_new = actor.lower().replace(' ', '-')
    url = 'https://letterboxd.com/actor/' + actor_new
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    actor_movies = soup.find_all("div", class_="poster")
    for movie in actor_movies:
      movie_url = 'https://letterboxd.com' + movie['data-film-link']
      print(movie_url)
      movie_page = requests.get(movie_url)
      movie_page_content = BeautifulSoup(movie_page.content, "html.parser")
      div = movie_page_content.find_all("div", class_='react-component')[1]
      movies.append(div["data-film-name"] + ", " + div["data-film-release-year"])
    with open("../lists/"+actor+".txt", 'w+') as f:
      for m in movies:
        f.write(m+'\n')
    movies = read_from_file(actor)
  return movies


def get_watched(login:str, reload:bool=False, title:str="Watched"):
  if reload:
    watched_url = 'https://letterboxd.com/' + login + '/films'

    movies = get_movies(watched_url)
    with open("../lists/" + title + ".txt", 'w') as f:
      for m in movies:
        f.write(m+'\n')
  movies = read_from_file(title)
  return movies  


def remove_nth_substring(string, sub, replacewith, n):
  where = [m.start() for m in re.finditer(sub, string)][n-1]
  before = string[:where]
  after = string[where:]
  after = after.replace(sub, replacewith, 1)
  newString = before + after
  return newString


def form_url(title:str, type:str, author:str = None) -> str:
  if type == 'list':
      if not author:
          return 'Error, input author'
      title = title.lower()
      title = title.replace(' ', '-') 
      title = title.replace('/', '-')
      title = title.replace('’', '')
      title = title.replace(':', '')
      title = title.replace('(', '').replace(')', '')
      title = title[:46]
      if author == 'ihamrasse':
        title = remove_nth_substring(title, 'top-', '', 2)
      author = author.lower()
      author = author.replace(' ', '')
      url = 'https://letterboxd.com/{}/list/{}/'.format(author, title)
      print(url)
  return url


def get_watchlist(login:str, reload:bool=False, title:str="Watchlist"):
  if reload:
    watchlist_url = 'https://letterboxd.com/' + login + '/watchlist'

    movies = get_movies(watchlist_url)
    with open("../lists/" + title + ".txt", 'w+') as f:
      for m in movies:
        f.write(m + '\n')
  movies = read_from_file(title)
  return movies


def get_director_movies(director:str, reload:bool=False):
  movies = []
  if reload:
    director_new = director.lower().replace(' ', '-')
    url = 'https://letterboxd.com/director/' + director_new
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    actor_movies = soup.find_all("div", class_="poster")
    for movie in actor_movies:
      movie_url = 'https://letterboxd.com' + movie['data-film-link']
      print(movie_url)
      movie_page = requests.get(movie_url)
      movie_page_content = BeautifulSoup(movie_page.content, "html.parser")
      div = movie_page_content.find_all("div", class_='react-component')[1]
      movies.append(div["data-film-name"] + ", " + div["data-film-release-year"])
    with open("../lists/"+director+".txt", 'w+') as f:
      for m in movies:
        f.write(m+'\n')
  movies = read_from_file(director)
  return movies


def compare_lists(lists:list, union:bool=True, union_of_lists:int=2, user:str="RMNT_",
                  exclude_watched:bool=False, exclude_my_watched=False, include_watched:bool=False, reload_watched:bool=False, watched_title:str="Watched",
                  watchlist:bool=False, reload_watchlist:bool=False, watchlist_title:str="Watchlist",
                  actors:list=None, reload_actors:bool=False,
                  directors:list=None, reload_directors:bool=False,
                  additional_files:list=None,
                  list_url:str = None, list_url_num:int=None,
                  random_movie:bool=False, random_movie_size:int=1) -> list:
    movies = []
    list_number = len(lists)
    for i, lst in enumerate(lists):
        lst, author = lst
        file_name = lst + " | " + author
        file_name = file_name.replace('/', '-')
        files = os.listdir("../lists/")
        if file_name+'.txt' not in files: 
          if list_url and i == list_url_num-1:
            url = "http://www.letterboxd.com/" + author + '/list/' + list_url
            print(url)
          else:
            url = form_url(lst, 'list', author)
          movie_list = get_movies(url)
          with open("../lists/" + file_name, 'w+') as f:
            for movie in movie_list:
              f.write(movie+'\n')
        else:
          movie_list = read_from_file(file_name)
        movies.extend(movie_list) 
    
    if not union:
      movies = list(set([m for m in movies if movies.count(m) > union_of_lists-1]))
    else:
      movies = list(set([m for m in movies if movies.count(m) > list_number-1]))
    
    if actors:
      for actor in actors:
        actor_movies = get_actor_movies(actor, reload=reload_actors)
        movies.extend(actor_movies)
      movies = list(set([m for m in movies if movies.count(m) > 1]))
    
    if directors:
      for director in directors:
        director_movies = get_director_movies(director, reload=reload_directors)
        movies.extend(director_movies)
      movies = list(set([m for m in movies if movies.count(m) > 1]))
    
    if exclude_watched:
      watched = get_watched(user, reload=reload_watched, title=watched_title)
      movies = list(np.setdiff1d(movies, watched))
    
    if exclude_my_watched:
      watched = get_watched('RMNT_', reload=reload_watched, title="Watched")
      movies = list(np.setdiff1d(movies, watched))
    
    if include_watched:
      watched = get_watched(user, reload=reload_watched, title=watched_title)
      movies.extend(watched)
      movies = list(set([m for m in movies if movies.count(m) > 1]))
    
    # Parašyti
    # if additional_files:
    #   for add_file in additional_files:
    #     pass
    #   movies = list(set([m for m in movies if movies.count(m) > 1]))
    
    if watchlist:
      movies.extend(get_watchlist(user, reload=reload_watchlist, title=watchlist_title))
      movies = list(set([m for m in movies if movies.count(m) > 1]))
    
    if '' in movies:
      movies.remove('')
    
    if random_movie:
      return random.sample(movies, random_movie_size)
    
    return movies