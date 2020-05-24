import argparse
import multiprocessing
from ssl import SSLCertVerificationError

import httplib2
import logging
import time
import threading
from bs4 import BeautifulSoup
from urllib.parse import urlparse

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

logger = logging.getLogger('chardet.charsetprober')
logger.setLevel(logging.INFO)
links_set = {'https://www.onet.pl'}
http = httplib2.Http()
timeout = time.time() + 60*5
set_lock = threading.Lock()
logger_lock = threading.Lock()
thread_count = 5


def is_absolute(url):
    return bool(urlparse(url).netloc)


def make_log(log: str):
    logger.warning(log)


def scrap_page_from_links(page_url: str):
    status, response = http.request(page_url)
    soup = BeautifulSoup(response)
    a_elements = soup.find_all("a")
    for a in a_elements:
        link = a.get("href")
        if is_absolute(link):
            links_set.add(link)


def get_link_from_set():
    with set_lock:
        return links_set.pop()


def generate_traffic():
    loops_made = 0
    while time.time() < timeout:
        link = get_link_from_set()
        try:
            scrap_page_from_links(link)
        except httplib2.RelativeURIError:
            make_log("Absolute url found")
        except SSLCertVerificationError:
            make_log("SSL certificate problem")
        except:
            make_log("Someting went wong")
        make_log(f"Scrapped {link}")
        loops_made += 1
        make_log(f"Scrapped {loops_made} links already")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('thread_count', type=int)
    parser.add_argument('test_time', type=int)
    args = parser.parse_args()
    timeout = time.time() + 60 * int(args.test_time)
    for i in range(int(args.thread_count)):
        t = multiprocessing.Process(target=generate_traffic)
        t.start()
