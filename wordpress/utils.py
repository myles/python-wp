from datetime import datetime


def parse_iso8601(string):
    return datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')
