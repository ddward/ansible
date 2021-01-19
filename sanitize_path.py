import re

def sanitize(path):
    # escape nasty double-dots
    path = re.sub(r'\.\.', '', path)
    # then remove any duplicate slashes
    path = re.sub(r'(/)\1+', r'\1', path)
    # then remove any leading slashes and dots
    while(path and (path[0] == '/' or path[0] == '.')):
        path = path[1:]
    return path