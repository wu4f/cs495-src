import aiohttp
from bs4 import BeautifulSoup
import time
import asyncio

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
        return elapsed
    return inner

async def agetUrlTitle(session, url):
    """
    This asynchronous function returns the <title> of an HTML document given its URL
    :param session: AIOHTTP session
    :param url: URL to retrieve
    :type url: str
    :return: Title of URL
    :rtype: str
    """
    try:
        async with session.get(url) as resp:
            text = await resp.text()
            soup = BeautifulSoup(text, 'html.parser')
            title = soup.find('title').text if soup.find('title') else 'No Title Found'
            return title
    except Exception as e:
        return f'Error: {e}'


async def async_main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [agetUrlTitle(session, url) for url in urls]
        return await asyncio.gather(*tasks)


@time_decorator
def getAsync(urls):
    """
    Given a list of URLs, retrieve the title for each one using a single synchronous process
    :param urls: List of URLs to retrieve
    :type urls: list of str
    :return: list of str
    """
    return asyncio.run(async_main(urls))


# Retrieve the list of URLs
import requests
resp = requests.get('https://thefengs.com/wuchang/courses/cs495/urls.txt')
urls = resp.text.split('\n')[:50]

# Fetch titles asynchronously
fetch_time = getAsync(urls)
print(f'Async version: {fetch_time:0.2f}')