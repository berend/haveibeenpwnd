python bindings for HaveIBeenPwnd.com V2
========================================

Troy Hunt released a new version of the `Have I Been pwnd Database`. This time with more anonymity
in mind.

Features:
---------

* does not sent passwords to HaveIBeenPwnd.com
* does not sent complete password hashes to HaveIBeenPwnd.com
* zero dependencies except requests (will be removed later)
* python2 & python3 support
* tests

Usage:
------

You can use HaveIBeenPwnd als command line script or use it as module in other python code.

As command line script
----------------------

Install HaveIBeenPwnd gobally or in a virtual environment:

    $ pip install haveibeenpwnd

This add shortcuts to haveibeenpwnd, so that you call haveibeenpwnd from everywhere. To check a
password, simply do this:

    $ haveibeenpwnd --password hunter2
    The password was found 16092 times in the haveibeenpwned.com database.

Remember, haveibeenpwnd does not send the given password into the internet, it sends the first 5
chars of the SHA1 Hash.

To check if a mail has been part of a breach, do this:


    $ haveibeenpwnd -m test@example.com
    The email <test@example.com> was found in following breaches:
    The <000webhost> breach (2015-03-01) exposed Email addresses, IP addresses, Names and Passwords
    The <8tracks> breach (2017-06-27) exposed Email addresses and Passwords
    ...


As module
---------

Check emails:

    >>> from haveibeenpwnd import check_email
    >>> check_email("test@example.com"))
    >>> check_email("test@example.com")
    {'breaches': [{'Title': '000webhost', ...}]}

and check passwords:

    >>> from haveibeenpwnd import check_password
    >>> check_password('hunter2')
    16092
    >>> check_password('lksdflksdpsökfdsödg')
    0

Installation
------------

You can install haveibeenpwnd with pip:

    $ pip install haveibeenpwnd


Testing:
--------

You can run tests with:

    $ tox

