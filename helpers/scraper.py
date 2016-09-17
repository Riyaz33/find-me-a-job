import json
import os
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from constants.endpoints import endpoints

BASE_URL = 'http://stackshare.io%s'


def fetch(url):
    return requests.get(url)


def parse_stack_contents(soup):
    header, description, stack, jobs = soup.find(id='stack-name'), \
        soup.find(id='stack-description'), \
        soup.find(class_='full-stack-container'), \
        soup.find(id='stack-jobs')

    name = header.find('span', {'itemprop': 'name'}).text.strip()
    tags = \
        [c.text.strip()
         for c in header.find_all('a', {'itemprop': 'applicationSubCategory'})]

    description = description.find('span', {'itemprop': 'description'}).text

    parsed_stack = {}

    for layer in stack.find_all('div', {'class': 'stack-layer'}):
        clss = None

        for c in layer['class']:
            if c not in ['stack-layer', 'show-layer-d']:
                clss = c

        parsed_stack[clss] = []

        for service in stack.find(class_=clss).find_all('div', {'id': 'stp-services'}):
            parsed_stack[clss].append({
                'name': service.find('a', {'class': 'stack-service-name-under'}).text.strip(),
                'type': service.find('a', {'class': 'function-name-under'}).text.strip()
            })

    parsed_jobs = []

    for col in jobs.find(class_='row').find_all(class_='col-md-6'):
        parsed_jobs.append({
            'title': col.find('div').text.strip().split('\n')[0],
            'description': col.find(class_='function-name-under').text.strip(),
            'link': col['onclick']
        })

    return {
        'name': name,
        'description': description,
        'tags': tags,
        'stack': parsed_stack,
        'available_jobs': parsed_jobs
    }


def main():
    response = []

    for ep in endpoints:
        try:
            html = fetch(BASE_URL % str(ep))
            soup = BeautifulSoup(html.text, 'html.parser')
            response.append(parse_stack_contents(soup))
        except Exception, e:
            continue

    return response


if __name__ == '__main__':
    res = main()
    print(json.dumps(res))
