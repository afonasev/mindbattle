#!/usr/bin/env python3
"""Print selected JSON pointers from a manifest without changing its source."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def select(document, pointer):
    if not pointer.startswith('/'):
        raise ValueError('Use a non-root JSON pointer starting with /: ' + pointer)
    value = document
    for part in pointer[1:].split('/'):
        if re.search(r'~(?![01])', part):
            raise ValueError('Invalid JSON pointer escape: ' + pointer)
        key = part.replace('~1', '/').replace('~0', '~')
        if isinstance(value, dict) and key in value:
            value = value[key]
        elif isinstance(value, list) and re.fullmatch(r'0|[1-9][0-9]*', key) and int(key) < len(value):
            value = value[int(key)]
        else:
            raise ValueError('Missing JSON pointer: ' + pointer)
    return value


def project(path, pointers, max_bytes=16000):
    if not pointers or max_bytes <= 0:
        raise ValueError('Select at least one field and a positive output byte limit')
    path = Path(path).resolve(strict=True)
    raw = path.read_bytes()
    document = json.loads(raw)
    result = {
        'source': {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest()},
        'projectionOnly': True,
        'fields': {pointer: select(document, pointer) for pointer in pointers},
    }
    output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if len(output.encode('utf-8')) > max_bytes:
        raise ValueError('Projection exceeds output byte limit; select narrower pointers. Nothing was truncated.')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('pointers', nargs='+', help='Exact JSON pointers, e.g. /CURRENT /claimsOwner /currentWork')
    parser.add_argument('--max-bytes', type=int, default=16000)
    args = parser.parse_args()
    try:
        output = project(args.manifest, args.pointers, args.max_bytes)
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + '\n')
    print(output, end='')


if __name__ == '__main__':
    main()
