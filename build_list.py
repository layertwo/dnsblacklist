#!/usr/bin/env python3
import functools
import json
import requests

def read_jsonl(filename):
    """
    Read jsonl file and return output
    """
    output = []
    with open(filename, 'r') as fp:
        for line in fp:
            output.append(json.loads(line))
    return output


@functools.lru_cache()
def process_url(line):
    line = line.decode('utf-8')
    if line and not line.startswith('#'):
        split = line.split()
        if len(split) > 1:
            if split[0] != '0.0.0.0':
                return ''
            return split[1]
        return split[0]
    return ''


def main():
    domains = set()
    lists = read_jsonl('domain-lists.jsonl')
    for dl in lists:
        req = requests.get(dl['url'], stream=True)
        for line in req.iter_lines():
            domain = process_url(line)
            if domain:
                domains.add(domain)

    with open('blacklist.conf', 'w') as fp:
        for domain in sorted(domains):
            fp.write('address=/{}/0.0.0.0\n'.format(domain))
        fp.close()


if __name__ == '__main__':
    main()
