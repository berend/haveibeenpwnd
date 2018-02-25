# -*- coding: utf-8 -*-
from hashlib import sha1
import requests

HEADERS = {'user-agent': 'pypi.org/project/haveibeenpwnd/ v0.1', 'api-version': 2}
range_url = 'https://api.pwnedpasswords.com/range/{}'
email_url = 'https://haveibeenpwned.com/api/v2/breachedaccount/{}'
error_messages = {
    400: "Bad request — the account does not comply with an acceptable format "
         "(i.e. it's an empty string)",
    403: "Forbidden — no user agent has been specified in the request",
    429: "Too many requests — the rate limit has been exceeded",
    526: "Cloudflare SSL Error - please try again later"
}


def check_password(password):
    hashed_password = sha1(password.encode('utf-8')).hexdigest()

    prefix = hashed_password[:5]
    suffix = hashed_password[5:]

    # only send a prefix of 5 chars to haveibeenpwnd.com
    response = requests.get(range_url.format(prefix), HEADERS).text

    for line in iter(response.splitlines()):
        hex, _, count = line.partition(':')
        if hex == suffix.upper():
            return {'count': int(count)}
    else:
        return {'count': 0}


def check_email(email):
    response = requests.get(email_url.format(email), HEADERS)
    http_status = response.status_code
    if http_status == 200:
        return {
            'breaches': response.json()
        }
    elif http_status == 404:
        return {'breaches': []}
    else:
        message = error_messages.get(http_status, "Unknown error: {}".format(http_status))
        return {
            'error': message,
            'breaches': ''
        }


def cli_check_email(email):
    response = check_email(email)
    if 'error' in response:
        print(response['error'])
    elif not response["breaches"]:
        print("The email <{}> was not found in a breach.".format(email))
    else:
        print("The email <{}> was found in following breaches:".format(email))
        for b in response['breaches']:
            print("The <{}> breach ({}) exposed {}".format(
                b['Name'], b['BreachDate'], list_to_print_string(b['DataClasses'])))


def list_to_print_string(l):
    if len(l) == 1:
        return l[0]
    else:
        return ", ".join(l[:-1]) + " and {}".format(l[-1])


def cli_check_password(password):
    count = check_password(password)['count']

    if count:
        print("The password was found {} times in the haveibeenpwned.com database.".format(count))
    else:
        print("The password was not found in the haveibeenpwned.com database.")


def run():
    import argparse
    pwd_help = '''Check haveibeenpwned.com if the given password has been discovered in a breach.
               Only 5 chars of the SHA1 hash of the password will be submitted to
               haveibeenpwned.com. If the password was found, it is either common and not secure,
               or it was part of a breach. Or both.'''
    email_help = '''Check haveibeenpwned.com if an email has been found in a breach. If it was
    found, you should make sure, that you update your password. You should also consider two
    factor auth if possible.
    '''

    description = '''Check your email or your password against an Online database of all known
    security breaches.
    '''

    epilog = '''For more information check https://haveibeenpwned.com/FAQs or
    https://github.com/berend/haveibeenpwnd.
    '''

    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('--password', '-p', help=pwd_help)
    parser.add_argument('--email', '-m',  help=email_help)

    args = parser.parse_args()

    if args.email:
        cli_check_email(args.email)
    if args.password:
        cli_check_password(args.password)


if __name__ == '__main__':
    run()
