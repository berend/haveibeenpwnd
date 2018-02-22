from hashlib import sha1
import requests


HEADERS = {'user-agent': 'pypi.org/project/haveibeenpwnd/ v0.1', 'api-version': 2}
range_url = 'https://api.pwnedpasswords.com/range/{}'


def check_password(password):
    hashed_password = sha1(password.encode('utf-8')).hexdigest()

    prefix = hashed_password[:5]
    suffix = hashed_password[5:]

    response = requests.get(range_url.format(prefix), HEADERS).text

    for line in iter(response.splitlines()):
        hex, _, count = line.partition(':')
        if hex == suffix.upper():
            return int(count)
    else:
        return 0
