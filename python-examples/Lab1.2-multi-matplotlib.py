import requests
from bs4 import BeautifulSoup
import time
import multiprocessing
import matplotlib.pyplot as plt


def time_decorator(func):
    """
  Takes a function and returns a version of it that prints out the elapsed time for executing it
  :param func: Function to decorate
  :return: Function which outputs execution time
  :rtype: Function
  """
    def inner(*args, **kwargs):
        s = time.perf_counter()
        return_vals = func(*args, **kwargs)
        elapsed = time.perf_counter() - s
        print(f'Function returned: {return_vals}')
        return (elapsed)

    return (inner)


def getUrlTitle(url):
    """
    This function returns the <title> of an HTML document given its URL
    :param url: URL to retrieve
    :type url: str
    :return: Title of URL
    :rtype: str
  """
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find('title'):
      return(soup.find('title').text)
    else:
      return ('')


@time_decorator
def getMulti(urls, num_processes):
    """
    Given a list of URLs, retrieve the title for each one using a single synchronous process
    :param urls: List of URLs to retrieve
    :type urls: list of str
    :param num_processes: Number of processes to use
    :type num_processes: int
    :return: list of str
    :rtype: list of str
    """
    p = multiprocessing.Pool(num_processes)
    titles = p.map(getUrlTitle, urls)
    p.close()
    return (titles)

if __name__ == '__main__':
  resp = requests.get('https://thefengs.com/wuchang/courses/cs495/urls.txt')
  urls = resp.text.strip().split('\n')
  
  concurrencies = [25, 20, 15, 10, 5, 2, 1]
  elapsed = []
  
  for c in concurrencies:
      fetch_time = getMulti(urls, c)
      elapsed.append(fetch_time)
      print(f'{c} {fetch_time:0.2f}')
  print(list(zip(concurrencies,elapsed)))
  
  plt.scatter(concurrencies, elapsed)
  plt.xlabel("Number of Processes")
  plt.ylabel("Retrieval Time")
  plt.title("wuchang multiprocessing plot")
  plt.show()
