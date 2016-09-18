import os
import re

from aggregate_resource_list import aggregate_resource_list
from convert_pdf_to_txt import convert_pdf_to_txt
from find_all_documents import find_all_documents

DOCS = find_all_documents()
RESOURCES = aggregate_resource_list(DOCS)


def organize_resources_by_company():
    skills = dict()

    for res in RESOURCES:
        skills[res] = set()

    for company in DOCS:
        for skill_type in company['stack']:
            for skill in company['stack'][skill_type]:
                if skill['name'] in skills:
                    try:
                        skills[skill['name']].add(str(company['name']))
                    except Exception, e:
                        continue

    return skills


def analyze_results(fp):
    if not os.path.isfile(fp):
        return None

    resume_txt = convert_pdf_to_txt(fp).lower()
    resources = organize_resources_by_company()

    user_companies = {}

    for res in resources:
        if res.lower() in resume_txt:
            for company in resources[res]:
                if company not in user_companies:
                    user_companies[company] = {
                        'count': 0,
                        'matches': []
                    }

                user_companies[company]['count'] += 1
                user_companies[company]['matches'].append(res)

    # os.remove(fp)
    return user_companies


if __name__ == '__main__':
    from pprint import pprint
    res = analyze_results('static/uploads/my resume.pdf')
    pprint(res)
