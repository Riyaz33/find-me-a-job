import json
import os
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup
from bson import SON
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

    name = None

    try:
        name = header.find('span', {'itemprop': 'name'}).text.strip()
    except Exception, e:
        pass

    tags = []

    try:
        tags = \
            [c.text.strip()
             for c in header.find_all('a', {'itemprop': 'applicationSubCategory'})]
    except Exception, e:
        pass

    img = None

    try:
        img = header.find('img', {'itemprop': 'image'})['src']
    except Exception, e:
        pass

    try:
        description = description.find('span', {'itemprop': 'description'}).text
    except Exception, e:
        pass

    parsed_stack = dict()

    try:
        for layer in stack.find_all('div', {'class': 'stack-layer'}):
            clss = None

            for c in layer['class']:
                if c not in ['stack-layer', 'show-layer-d']:
                    clss = c

            parsed_stack[clss] = []

            for service in stack.find(class_=clss).find_all('div', {'id': 'stp-services'}):
                parsed_stack[clss].append(dict([
                    ('name', service.find('a', {'class': 'stack-service-name-under'}).text.strip()),
                    ('type', service.find('a', {'class': 'function-name-under'}).text.strip())
                ]))
    except Exception, e:
        pass

    parsed_jobs = []

    try:
        for col in jobs.find(class_='row').find_all(class_='col-md-6'):
            parsed_jobs.append(dict([
                ('title', col.find('div').text.strip().split('\n')[0]),
                ('description', col.find(class_='function-name-under').text.strip()),
                ('link', col['onclick'])
            ]))
    except Exception, e:
        pass

    return dict([
        ('name', name),
        ('description', description),
        ('tags', tags),
        ('img', img),
        ('stack', parsed_stack),
        ('available_jobs', parsed_jobs)
    ])


def main():
    client = MongoClient('mongodb://localhost:27017', document_class=SON)
    db = client.fmajil

    db.stacks.delete_many({})

    response = []

    i = 1

    for ep in endpoints:
        print 'Scraping', i
        try:
            html = fetch(BASE_URL % str(ep))
            soup = BeautifulSoup(html.text, 'html.parser')
            contents = parse_stack_contents(soup)
            response.append(contents)
            db.stacks.insert_one(contents.copy())
            print 'Scraped', i
        except Exception, e:
            print 'Failed', i
            print(e)
            continue

        i += 1

    client.close()
    return response


if __name__ == '__main__':
    from pprint import pprint

    res = main()
    pprint(json.dumps(res))
