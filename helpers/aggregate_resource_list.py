def aggregate_resource_list(stack_list):
    resources = set()
    for stack in stack_list:
        for stack_type in stack['stack']:
            for resource in stack['stack'][stack_type]:
                resources.add(str(resource['name']))
    return resources

if __name__ == '__main__':
    from pprint import pprint
    from find_all_documents import find_all_documents

    docs = find_all_documents()
    pprint(aggregate_resource_list(docs))
