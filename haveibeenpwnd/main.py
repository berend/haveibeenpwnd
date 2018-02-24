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

def check_email(email):
    pass  # on the roadmap


if __name__ == '__main__':
    import argparse
    pwd_help = '''Check HaveIbeenpwnd if the given password has been discovered in a breach.
               Only 5 chars of the SHA1 hash of the password will be submitted to HaveIbeenPwnd.
               
               If your password was found, it is either common and not secure, or it was part 
               of a breach. Or both.'''
    email_help = '''Check if an email has been found in a breach. If it was found, you should 
    make sure, that you update your password. You should also consider 2 factor auth if possible.
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--password', help=pwd_help)
    parser.add_argument('--email', help=email_help)
    
    args = parser.parse_args()

