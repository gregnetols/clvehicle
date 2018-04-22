import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, URLError
import random


def get_parameters():

    make = input("Enter the make of the vehicle to search: ")
    model = input("Enther the model to search: ")

    return make, model


def result_size_wait(results_size):
    seconds = results_size / 2.0
    print("waiting %5i seconds" % seconds)
    time.sleep(seconds)

def get_proxies():

    ua = UserAgent()
    proxies = []

    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'ip': row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })

    return proxies


def validate_proxy(proxy):

    test_request = Request('http://icanhazip.com')
    test_request.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

    try:
        my_ip = urlopen(test_request).read().decode('utf8').rstrip('\n')
        valid_proxy = (my_ip == proxy['ip'])

    except:
        valid_proxy = False

    return valid_proxy


def random_proxy(proxies):
    return proxies[random.randint(0, len(proxies) - 1)]


def select_proxy(proxies):

    while len(proxies) > 0:
        proxy = random_proxy(proxies)
        if validate_proxy(proxy):
            return proxy
        else:
            while proxy in proxies:
                proxies.remove(proxy)

    return None


