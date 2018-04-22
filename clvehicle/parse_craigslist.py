from bs4 import BeautifulSoup as bs4
from urllib.request import urlopen, Request
import requests
import pandas as pd
import re
import time
import utilities
import random


def parse_results(results):
    parsed_results = []
    idx = 0

    for idx, item in enumerate(results):

        item_dict = dict(item)
        parsed_results.append(item_dict)

    print('%9i Results found' %  idx)
    utilities.result_size_wait(idx)
    parsed_results = pd.DataFrame(parsed_results)

    return parsed_results


def parse_vehicle_urls(results):
    print('Parsing the ads')

    vehicle_list = []
    proxies = utilities.get_proxies()

    for k, url in enumerate(results['url']):
        vehicle = dict()

        # On the first and every 10 url hits switch proxy
        if k == 0 or k % 10 == 0:
            proxy = utilities.select_proxy(proxies)

        for column_name in results.columns:
            vehicle[column_name] = results[column_name].iloc[k]

        rsp = Request(url)
        rsp.set_proxy(proxy['ip'] + ':' + proxy['port'])
        raw_html = urlopen(rsp)
        html = bs4(raw_html, 'html.parser')

        try:
            vehresults = html.body.find_all('p', attrs={'class':'attrgroup'})

            try:
                vyear = vehresults[0].find_all('span')[0].get_text()[0:4]
                vehicle['Year'] = vyear

                vehicle_info = vehresults[1].find_all('span')
                for l in range(len(vehicle_info)):
                    try:
                        attribute, value = vehicle_info[l].get_text().split(':')
                    except ValueError:
                        print('Post %9i has a bad attribute - URL: %s'%(k, url))
                    vehicle[attribute] = value

                vehicle_list.append(vehicle)

            except IndexError:
                print('Post %9i was likely deleted - URL: %s'%(k, url))
        except AttributeError:
            print('Post %9i has no attributes - URL: %s'%(k, url))

        time.sleep(1)

    return vehicle_list


#Parse the different sites available from the craigslist US sites page No site links on: https://geo.craigslist.org/iso/us
def parse_craigslist_sites():
    sites = []
    us_sites_list_url = 'https://geo.craigslist.org/iso/us'

    html = urlopen(us_sites_list_url)
    us_sites_html = bs4(html, 'html.parser')

    try:
        links = us_sites_html.find("ul", {"class": "height6 geo-site-list"})

        for link in links.findAll("a", href=True):
            us_site = re.search(r'https:\/\/(.*?).craigslist.org', link['href']).group(1)

            sites.append(us_site)

    except AttributeError:
        print("No site links on: https://geo.craigslist.org/iso/us")

    return sites




