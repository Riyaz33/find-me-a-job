import json
import os
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from endpoints import endpoints

BASE_URL = 'http://stackshare.io%s'


def fetch(url):
    return requests.get(url)


def parse_stack_contents(soup):
    header, description, stack, jobs = soup.find(id='stack-name'), \
        soup.find(id='stack-description'), \
        soup.find(class_='full-stack-container'), \
        soup.find(id='stack-jobs')

    try:
        name = header.find('span', {'itemprop': 'name'}).text.strip()
    except Exception, e:
        pass

    try:
        tags = \
            [c.text.strip()
             for c in header.find_all('a', {'itemprop': 'applicationSubCategory'})]
    except Exception, e:
        pass

    try:
        img = header.find('img', {'itemprop': 'image'})['src']
    except Exception, e:
        pass

    try:
        description = description.find('span', {'itemprop': 'description'}).text
    except Exception, e:
        pass

    parsed_stack = {}

    try:
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
    except Exception, e:
        pass

    parsed_jobs = []

    try:
        for col in jobs.find(class_='row').find_all(class_='col-md-6'):
            parsed_jobs.append({
                'title': col.find('div').text.strip().split('\n')[0],
                'description': col.find(class_='function-name-under').text.strip(),
                'link': col['onclick']
            })
    except Exception, e:
        pass

    return {
        'name': name,
        'description': description,
        'tags': tags,
        'img': img,
        'stack': parsed_stack,
        'available_jobs': parsed_jobs
    }


def main():
    client = MongoClient('mongodb://localhost:27017')
    db = client.fmajil

    response = []

    for ep in endpoints:
        try:
            html = fetch(BASE_URL % str(ep))
            soup = BeautifulSoup(html.text, 'html.parser')
            contents = parse_stack_contents(soup)
            db.stacks.insert_one(contents)
            response.append(contents)
        except Exception, e:
            print(e)
            continue

    client.close()
    return response


if __name__ == '__main__':
    res = main()
    print(json.dumps(res))
